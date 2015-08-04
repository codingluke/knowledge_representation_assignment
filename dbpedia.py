# coding: utf-8

import urllib, urllib2, json
import traceback, sys

def dbpedia_sparql_query(q, endpoint='http://dbpedia.org/sparql', f='application/json'):
    """
    Sends a GET-request to a given sparql endpoint with a given query.
    Returns the result as a JSON string.
    """
    try:
        params = {'query': q}
        params = urllib.urlencode(params)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(endpoint + '?' + params)
        request.add_header('Accept', f)
        request.get_method = lambda: 'GET'
        url = opener.open(request)
        return url.read()
    except Exception, e:
        traceback.print_exc(file=sys.stdout)
        raise e 

def dbpedia_person(name):
    """
    Queries a person by name at dbpedia. 
    Returns the dbpedia persons uris as array.
    """
    q = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?person ?abstract
        WHERE {
            ?person foaf:name ?name .
            ?person dbo:abstract ?abstract .
            FILTER(
                str(?name) = \"""" + name + """\" && 
                langMatches(lang(?abstract),"de") 
            )
        }"""
    result = dbpedia_sparql_query(q)
    j = json.loads(result, parse_float=True, parse_int=True)
    return [ ( p['person']['value'], p['abstract']['value'] ) for p in j['results']['bindings'] ]
