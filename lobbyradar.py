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

