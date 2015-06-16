#from pymongo import MongoClient

#con = MongoClient()
#entities = con.lobbyradar.entities
#cursor = entities.find({})

# mongorestore --host dumbo01.f4.htw-berlin.de --db herta --collection entities entities.bson  -p YourPassWord -u herta --port=27020

# mongorestore --host dumbo01.f4.htw-berlin.de --db herta --collection relations relations.bson  -p YourPassWord -u herta --port=27020

# on local instance:
# sudo service mongod start

#http://docs.mongodb.org
#http://api.mongodb.org/python/current/tutorial.html

import pymongo
from pymongo import MongoClient

client = MongoClient()

db = client.lobbyradar

#remote db on HTW

#client = MongoClient('mongodb://dumbo01.f4.htw-berlin.de:27020/')
#db = client.herta
#db.authenticate('herta', 'password')


# two collections available
# entities, relations
db.collection_names()



db.entities.find_one()


db.entities.count()


entity_cursor = db.entities.find()
entity_cursor.next()

db.entities.distinct("type")

#
db.relations.find_one()
#
db.relations.count()

relation_cursor = db.relations.find()
relation_cursor.next()


db.relations.distinct("type")


from bson.son import SON
pipeline = [ {"$group": {"_id": "$type", "counter": {"$sum": 1}}} , {"$sort": SON([("counter", -1), ("_id", -1)])} ]

list(db.entities.aggregate(pipeline))

list(db.relations.aggregate(pipeline))

pipeline = [ {"$group": {"_id": "$importer", "count": {"$sum": 1}}} , {"$sort": {"count":1} }]
list(db.entities.aggregate(pipeline))


import pprint
pp = pprint.PrettyPrinter(indent=2)
for i in db.relations.find({"type":"Tochterfirma"}):
    pp.pprint(i)
    print "######################################"

query = {'type':'entity', 'importer':'parteispenden14'}
projection = {'_id':0, 'name':1}
for i in db.entities.find(query, projection):
    pp.pprint(i)

db.entities.find(query, projection).count()


## Operators
# Operators have a leading '$'
# e.g. $gt : greater than
# http://docs.mongodb.org/manual/reference/operator/
# http://docs.mongodb.org/manual/reference/operator/query/

# query constraint as subdocument
query = {'name': {'$gte': 'X', '$lte': 'Z'} }
projection = {'_id':0, 'name':1}
for i in db.entities.find(query, projection):
    pp.pprint(i)

from datetime import datetime
query = {'updated': {'$gte': datetime(2015,4,29), '$lte': datetime(2015,5,3)} }
for i in db.entities.find(query):
    pp.pprint(i)

# Operators:
# $exists: 0 or 1 checks if a filed exists
# $regex
# ...

# Query on a array fields (here tags field)
query = {'tags': "representative"}
db.entities.find_one(query)
# $in operator : any of the provided values should match
query = {'tags': {'$in':["representative", "Medien"]}}
db.entities.find_one(query)
#
query = {'tags': {'$all':["lobbyismus", "Medien"]}}
db.entities.find_one(query)
# in compararion with
db.entities.find({'tags': "Medien"}).count()
db.entities.find({'tags': "lobbyismus"}).count()

# dot notation for querying inner documents or projection
projection = {'data.format'}
db.entities.find_one({}, projection)


pipeline = [ {"$group": {"_id": "$importer", "count": {"$sum": 1}}} , {"$sort": {"count":1} }]
list(db.entities.aggregate(pipeline, cursor={}))


pipeline = [ {"unwind": "data"} ]

#[{"$group": {"_id": "$importer", "count": {"$sum": 1}}} ,
             #{"$sort": {"count":1} }]

p = db.entities.aggregate(pipeline)

pipeline = [ {"$unwind": "$data"} , {"$group": {"_id": "$data.key", "count":{"$sum": 1}}}, {"$sort": {"count":-1}}]
list(db.entities.aggregate(pipeline, cursor={}))


def get_cursor_given_key_value(key):
    assert type(key) == str
    pipeline = [ {"$unwind": "$data"} , {"$match": { "data.key": key}}, {"$limit":10}]
    return db.entities.aggregate(pipeline, cursor={})




