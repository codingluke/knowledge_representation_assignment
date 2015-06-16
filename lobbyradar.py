import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.lobbyradar

Entities = db.entities
Relations = db.relations

persons = Entities.find({'type' : 'person'})
entities = Entities.find({'type' : 'entity'})

