# coding: utf-8

import pymongo
from pymongo import MongoClient
from bson.son import SON
from bson.objectid import ObjectId
import rdflib
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

client = MongoClient()
db = client.lobbyradar

Entities = db.entities
Relations = db.relations

person_filter = { 'type' : 'person' }
entity_filter = { 'type' : 'entity' }
persons = Entities.find(person_filter)
entities = Entities.find(entity_filter)


# executive, ececutive, Vorsitzender
directors_board_members = ['Aufsichtsratsmitglied', 'Board of Directors', 'Mitglied des Aufsichtsrats', 'Mitglied im Aufsichtsrat', 'Lenkungsgruppe', 'Mitglied des Aufsichtsrates', 'Anteilseignervertreter', 'Stellvertretender Vorstandsvorsitzender des Aufsichtsrats']
management_board_members = ['Vorstandsmitglied', 'Mitglied des Vorstands']
presidial_board_members = ['Präsidialmitglied', 'Mitglied des Präsidiums', 'Präsidiumsmitglied']
chairmen_of_management = ['Vorstandsvorsitz', 'Vorstandsvorsitzender', 'Vorsitzender des Vorstands']
management_members = ['Vorstand']
chairmen_of_directors_board = ['Aufsichtsratsvorsitz', 'Vorsitzender des Aufsichtsrats']
foundation_board_members = ['Mitglied des Stiftungsrats', 'Stiftungsrat']
directors = ['Geschäftsführer', 'Hauptgeschäftsführer', 'CEO', 'Geschäftsführender Vorstand', 'Geschäftsführender Gesellschafter', 'Direktor']
presidents = ['Präsident', 'Vorsitz', 'Vorsitzender', 'Präsidentin']
trustees_board_members = ['Mitglied des Kuratoriums']
advidory_board_members = ['Mitglied im Beirat', 'Mitglied des Beirats', 'Beisitzer des Beirats']
vice_presidents = ['Stellvertretender Vorsitz', 'Vize-Präsident', 'Vizepräsident']
administration_board_members = ['Mitglied des Verwaltungsrats']


# In[4]:

# member, activity, position
ordinary_members = ['Ordentliches Mitglied']
representative_members = ['Stellvertretendes Mitglied']
chairmen = ['Obmann']
chairwomen = ['Obfrau']
alliance_members = ['Mitglied im Verband']
honorary_members = ['Ehrenmitglied']


# In[5]:

# government, Bundesdatenschutzbeauftragte
ministers = ['Staatsminister', 'Staatsministerin', 'Bundesminister für Umwelt, Naturschutz und Reaktorsicherheit', 'Bundesministerin für Familie, Senioren, Frauen und Jugend', 'Bundesminister für Wirtschaft und Technologie', 'Minister für Inneres und Kommunales', 'Minister für Inneres und Sport', 'Bundesminister für Ernährung, Landwirtschaft und Verbraucherschutz', 'Bundesministerin für Bildung, Wissenschaft, Forschung und Technologie', 'Bundesminister für besondere Aufgaben', 'Bundesminister für Arbeit und Soziales', 'Bundesminister des Auswärtigen', 'Bundesminister des Inneren', 'Minister für Umwelt und Verbraucherschutz', 'Bundesminister für Verbraucherschutz', 'Ernährung und Landwirtschaft', 'Minister der Justiz und für Verbraucherschutz', 'Bundesminister für Verkehr, Bau und Stadtentwicklung', 'Staatsrätin für Bundesangelegenheiten, Europa und Integration', 'Ministerin für Arbeit, Gleichstellung und Soziales', 'Minister für Energie, Infrastruktur und Landesentwicklung', 'Ministerin für Kultus', 'Ministerin für Schule und Berufsbildung', 'Senator für Inneres und Sport', 'Ministerin für Bildung, Wissenschaft, Weiterbildung und Kultur', 'Minister für Wirtschaft, Arbeit und Verkehr', 'Ministerin für Arbeit, Soziales, Gesundheit, Frauen und Familie']
secretaries_of_states = ['Staatssekretär', 'Parlamentarischer Staatssekretär', 'Parlamentarische Staatssekretärin', 'Staatssekretärin']
privy_counselors = ['Staatsrat', 'Staatsrätin']
prime_ministers = ['Ministerpräsident', 'Ministerpräsidentin']
heads_of_state_chancellery = ['Chef der Staatskanzlei']
representatives_of_federal_chancellor = ['Stellvertreter der Bundeskanzlerin']
ministers_of_defense = ['Bundesminister der Verteidigung']
representatives_of_prime_minister = ['Stellvertretender Ministerpräsident', 'Stellvertreter des Ministerpräsidenten', 'Stellvertretende Ministerpräsidentin']
finance_ministers = ['Bundesminister der Finanzen', 'Finanzminister', 'Minister der Finanzen ']
justice_ministers = ['Minister der Justiz', 'Bundesministerin der Justiz', 'Justizministerin']


# In[6]:

import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF, SKOS
ORG = Namespace("http://www.w3.org/ns/org#")
OWN = Namespace("http://example.org/")

# The Graph
g = Graph()
g.bind("dc", DC)
g.bind("foaf", FOAF)
g.bind("org", ORG)
g.bind("skos", SKOS)
g.bind("own", OWN)

g.parse('ontology.ttl', format='turtle')

for entity in Entities.find({}):
    node = BNode()
    # DC
    g.add((node, DC.identifier, Literal(entity["_id"])))
    g.add((node, DC.created, Literal(entity["created"])))
    g.add((node, DC.modified, Literal(entity["updated"])))

    # RDF
    if entity['type'] == 'person':
        g.add((node, RDF.type, FOAF.Person))
        g.add((node, FOAF.name, Literal(entity["name"])))

    elif entity['type'] == 'entity':
        g.add((node, RDF.type, ORG.Organization))
        g.add((node, SKOS.prefLabel, Literal(entity["name"])))
        for alias in entity["aliases"]:
            g.add((node, SKOS.altLabel, Literal(alias)))

    # FOAF
    for tag in entity['tags']:
        g.add((node, FOAF.topic_intest, Literal(tag)))


# In[7]:

# Add executive relations
for rel in Relations.find({ 'type' : { '$in' : ['executive', 'ececutive', 'Vorsitzender'] }}):
    pos = [ attr['value'] for attr in rel['data'] if attr['key'] == 'position' ]
    pos = pos[0].encode('utf-8') if pos else ''.encode('utf-8')
    dest_node = g.value(predicate=DC.identifier, object=Literal(str(rel['entities'][0])))
    target_node = g.value(predicate=DC.identifier, object=Literal(str(rel['entities'][1])))

    if dest_node and target_node:
        # dest and target must be here
        dest_type = g.value(subject=dest_node, predicate=RDF.type)
        target_type = g.value(subject=target_node, predicate=RDF.type)

        if dest_type != target_type:
            # dest and target can not have the same tye
            if (dest_type == ORG.Organization) and (target_type == FOAF.Person):
                # the subject must be the person
                dest_node, target_node = target_node, dest_node

            if pos in directors_board_members:
                g.add((dest_node, OWN.isDirectorsBoardMemberOf, target_node))
            elif pos in management_board_members:
                g.add((dest_node, OWN.isManagementBoardMemberOf, target_node))
            elif pos in presidial_board_members:
                g.add((dest_node, OWN.isPresidialBoardMemberOf, target_node))
            elif pos in chairmen_of_management:
                g.add((dest_node, OWN.isChairmenOfManagement, target_node))
            elif pos in management_members:
                g.add((dest_node, OWN.isManagementMember, target_node))
            elif pos in chairmen_of_directors_board:
                g.add((dest_node, OWN.isChairmanOfDirectorsBoardOf, target_node))
            elif pos in foundation_board_members:
                g.add((dest_node, OWN.isFoundationBoardMemberOf, target_node))
            elif pos in directors:
                g.add((dest_node, OWN.isDirectorOf, target_node))
            elif pos in presidents:
                g.add((dest_node, OWN.isPresidentOf, target_node))
            elif pos in trustees_board_members:
                g.add((dest_node, OWN.isTrusteesBoardMemberOf, target_node))
            elif pos in advidory_board_members:
                g.add((dest_node, OWN.isAdvisoryBoardMemberOf, target_node))
            elif pos in vice_presidents:
                g.add((dest_node, OWN.isVicePresidentOf, target_node))
            elif pos in administration_board_members:
                g.add((dest_node, OWN.isAdministrationBoardMemberOf, target_node))
            else:
                g.add((dest_node, OWN.isOtherExecutiveOf, target_node))


# In[8]:

# Add member relations
for rel in Relations.find({ 'type' : { '$in' : ['member', 'activity', 'position'] }}):
    pos = [ attr['value'] for attr in rel['data'] if attr['key'] == 'position' ]
    pos = pos[0].encode('utf-8') if pos else ''.encode('utf-8')
    if len(rel['entities']) == 2:
        dest_node = g.value(predicate=DC.identifier, object=Literal(str(rel['entities'][0])))
        target_node = g.value(predicate=DC.identifier, object=Literal(str(rel['entities'][1])))

        if dest_node and target_node:
            # dest and target must be here
            dest_type = g.value(subject=dest_node, predicate=RDF.type)
            target_type = g.value(subject=target_node, predicate=RDF.type)

            if dest_type != target_type:
                # dest and target can not have the same tye
                if (dest_type == ORG.Organization) and (target_type == FOAF.Person):
                    # the subject must be the person
                    dest_node, target_node = target_node, dest_node

                if pos in ordinary_members:
                    g.add((dest_node, OWN.isOrdinaryMemberOf, target_node))
                elif pos in representative_members:
                    g.add((dest_node, OWN.isRepresentativeMemberOf, target_node))
                elif pos in chairmen:
                    g.add((dest_node, OWN.isChairmanOf, target_node))
                elif pos in chairwomen:
                    g.add((dest_node, OWN.isChairwomanOf, target_node))
                elif pos in alliance_members:
                    g.add((dest_node, OWN.isAllianceMemberOf, target_node))
                elif pos in honorary_members:
                    g.add((dest_node, OWN.isHonoraryMemberOf, target_node))
                else:
                    g.add((dest_node, OWN.isOtherMemberOf, target_node))


# In[9]:

# Add government relations
for rel in Relations.find({ 'type' : { '$in' : ['government', 'Bundesdatenschutzbeauftragte'] }}):
    pos = [ attr['value'] for attr in rel['data'] if attr['key'] == 'position' ]
    pos = pos[0].encode('utf-8') if pos else ''.encode('utf-8')
    if len(rel['entities']) == 2:
        dest_node = g.value(predicate=DC.identifier, object=Literal(str(rel['entities'][0])))
        target_node = g.value(predicate=DC.identifier, object=Literal(str(rel['entities'][1])))

    if dest_node and target_node:
            # dest and target must be here
            dest_type = g.value(subject=dest_node, predicate=RDF.type)
            target_type = g.value(subject=target_node, predicate=RDF.type)

            if dest_type != target_type:
                # dest and target can not have the same tye
                if (dest_type == ORG.Organization) and (target_type == FOAF.Person):
                    # the subject must be the person
                    dest_node, target_node = target_node, dest_node
                # target organisation must be a governmental organisation
                g.add((target_node, RDF.type, OWN.Government))

                if pos in secretaries_of_states:
                    g.add((dest_node, OWN.isSecretaryOfStateOf, target_node))
                elif pos in privy_counselors:
                    g.add((dest_node, OWN.isPrivyCouncilorOf, target_node))
                elif pos in ministers:
                    g.add((dest_node, OWN.isMinisterOf, target_node))
                elif pos in prime_ministers:
                    g.add((dest_node, OWN.isPrimeMinisterOf, target_node))
                elif pos in heads_of_state_chancellery:
                    g.add((dest_node, OWN.isHeadOfStateChancelleryOf, target_node))
                elif pos in representatives_of_federal_chancellor:
                    g.add((dest_node, OWN.isRepresentativeOfFederalChancellor, target_node))
                elif pos in ministers_of_defense:
                    g.add((dest_node, OWN.isMinisterOfDefenseOf, target_node))
                elif pos in representatives_of_prime_minister:
                    g.add((dest_node, OWN.isRepresentativeOfPrimeMinisterOf, target_node))
                elif pos in finance_ministers:
                    g.add((dest_node, OWN.isFinanceMinisterOf, target_node))
                elif pos in justice_ministers:
                    g.add((dest_node, OWN.isJusticeMinisterOf, target_node))
                else :
                    g.add((dest_node, OWN.isOtherwiseRelatedToGovernment, target_node))


# In[25]:

def search_persons(name="", limit=100):
    qres = g.query("""
    SELECT DISTINCT ?name
    WHERE {
          ?person rdf:type foaf:Person .
          ?person foaf:name ?name .
          FILTER(regex(lcase(str(?name)), \"""" + name.lower() + """\", "i"))
    }
    LIMIT """ + str(limit))
    return [ name[0].toPython() for name in qres ]


# In[11]:

def search_sparql(query):
    return g.query(query)


# In[12]:

def search_governmental(name = ""):
    qres = g.query("""
    SELECT DISTINCT ?name
    WHERE {
          ?org rdf:type own:Government .
          ?org skos:prefLabel ?name .
          FILTER(regex(lcase(str(?name)), \"""" + name.lower() + """\", "i")) .
    }
    LIMIT 100
    """)
    return [ name[0].toPython() for name in qres ]


# In[13]:

def search_organizations(name = ""):
    qres = g.query("""
    SELECT DISTINCT ?name
    WHERE {
          ?org rdf:type org:Organization .
          ?org skos:prefLabel ?name .
          FILTER(regex(lcase(str(?name)), \"""" + name.lower() + """\", "i")) .
    }
    LIMIT 100
    """)
    return [ name[0].toPython() for name in qres ]


# In[14]:

def person_connections(name):
    qres = g.query("""
    SELECT DISTINCT ?aname ?property ?bname
    WHERE {
        {
            ?p rdfs:isSubPropertyOf own:isMemberOf .
            ?property rdfs:isSubPropertyOf ?p .
            ?a ?property ?b .
            ?a foaf:name ?aname .
            ?b skos:prefLabel ?bname .
        }
        UNION
        {
            ?property rdfs:isSubPropertyOf own:isMemberOf .
            ?a ?property ?b .
            ?a foaf:name ?aname .
            ?b skos:prefLabel ?bname .
        }
        FILTER(lcase(str(?aname)) = \"""" + name.lower() + """\") .
    }
    LIMIT 100""")
    return [ (row[0].toPython(), row[1].toPython(), row[2].toPython()) for row in qres ]


# In[15]:

def organization_connections(name):
    qres = g.query("""
    SELECT DISTINCT ?aname ?property ?bname
    WHERE {
        {
            ?p rdfs:isSubPropertyOf own:isMemberOf .
            ?property rdfs:isSubPropertyOf ?p .
            ?a ?property ?b .
            ?a foaf:name ?aname .
            ?b skos:prefLabel ?bname .
        }
        UNION
        {
            ?property rdfs:isSubPropertyOf own:isMemberOf .
            ?a ?property ?b .
            ?a foaf:name ?aname .
            ?b skos:prefLabel ?bname .
        }
        FILTER(lcase(str(?bname)) = \"""" + name.lower() + """\") .
    }
    LIMIT 100""")
    return [ (row[0].toPython(), row[1].toPython(), row[2].toPython()) for row in qres ]


# In[16]:

def plot_tripples(connections_triple, figsize=(20,10)):
    """Plottet tripples in einem einfachen Graph"""
    G = nx.Graph()
    for obj, prt, sub in connections_triple:
        G.add_node(obj, typ='obj')
        G.add_node(sub, typ='sub')
        G.add_edge(obj, sub, label=prt)
    colors = [ 'green' if G.node[node]['typ'] == 'obj' else 'red' for node in G.nodes() ]
    plt.rcParams['figure.figsize'] = figsize
    plt.rcParams['font.family'] = 'sans-serif'
    nx.draw_networkx(G, node_color=colors, node_size=1000, linewidths=0, font_size=16)
