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

projection = {'_id':0, 'name':1}
for person in Entities.find(person_filter, projection):
    node = BNode()
    g.add((node, RDF.type, FOAF.Person))
    g.add((node, FOAF.name, Literal(person["name"])))

projection = {'_id':0, 'name':1}
for entity in Entities.find(entity_filter, projection):
    node = BNode()
    g.add((node, RDF.type, ORG.Organization))
    g.add((node, SKOS.prefLabel, Literal(entity["name"])))

