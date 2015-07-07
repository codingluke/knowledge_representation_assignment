import pymongo
from pymongo import MongoClient

import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF, SKOS
ORG = Namespace("http://www.w3.org/ns/org#")

client = MongoClient()
db = client.lobbyradar

Entities = db.entities
Relations = db.relations

person_filter = { 'type' : 'person' }
entity_filter = { 'type' : 'entity' }
persons = Entities.find(person_filter)
entities = Entities.find(entity_filter)

# The Graph
g = Graph()
g.bind("dc", DC)
g.bind("foaf", FOAF)
g.bind("org", ORG)
g.bind("skos", SKOS)

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

import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
ORG = Namespace("http://www.w3.org/ns/org#")

class lobbyPerson:
    """RDF-iable person object from lobbyradar person"""
    def __init__(self, person):
        if (person['type'] == 'person'):
            self.name = person.get('name')
            self.created = person.get('created')
            self.id = person.get('_id')

    def addToRDFGraph(self, graph):
        p = BNode()
        graph.add((p, RDF.type, FOAF.Person))
        graph.add((p, FOAF.name, Literal(self.name)))
        graph.add((p, DC.created, Literal(self.created)))
        graph.add((p, DC.identifier, Literal(self.id)))
        
class lobbyEntity:
    """RDF-iable entity object from lobbyradar person"""
    def __init__(self, entity):
        if (entity['type'] == 'entity'):
            self.name = entity.get('name')
            self.created = entity.get('created')
            self.id = entity.get('_id')

    def addToRDFGraph(self, graph):
        person = BNode()
        graph.add((person, RDF.type, ORG.Organization))
        graph.add((person, FOAF.name, Literal(self.name)))
        graph.add((person, DC.created, Literal(self.created)))
        graph.add((person, DC.identifier, Literal(self.id)))

g = rdflib.Graph()

for i in range(1, 10):
    person = lobbyPerson(persons.next())
    person.addToRDFGraph(g)

for i in range(1, 10):
    entity = lobbyEntity(entities.next())
    entity.addToRDFGraph(g)

print("--- printing raw triples ---")
for s, p, o in g:
    print((s, p, o))
