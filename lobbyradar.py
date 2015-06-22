import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.lobbyradar

Entities = db.entities
Relations = db.relations

persons = Entities.find({'type' : 'person'})
entities = Entities.find({'type' : 'entity'})

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
    """RDF-iable person object from lobbyradar person"""
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