# Knowledge Representation

# Dependencies

## Python

- ipython
- pymongo
- bson
- rdflib
- networkx
- matplotlib

## MongoDB
Mongodb muss installiert sein und zusätzlich dazu die Datenbank vom lobbyradar.

[Lobbyradar](https://github.com/lobbyradar/lobbyradar)
[Lobbyradar dump](https://github.com/lobbyradar/dumps)

# Starten des Programs

Am Besten über `ipython notebook`

## Notebooks

__BenutzungLobbyRadar.ipynb:__
Script welches die Benutzung der Programmes aufzeigt.

__Graph.ipynb:__
Die Erstellung des RDF-Graph und definitionen der Abfragefunktionen.

__Ontology.ipynb:__
Verwendete Scripte zur Durchsuchung der MongoDB um eine Ontologie ab zu leiten.

__dbpedia.ipynb:__
Definitionen der dbpedia Abfragefunkonen.

## Python scripte

__Graph.py:__
Die erstellung des RDF-Graph und definitionen der Abfragefunktionen als
python Datei zur Verwendung.

__dbpedia.py:__
Definitionen der dbpedia Abfragefunkonen zur Verwendung

__ontology.ttl:__ Eigene Ontologie im Turtleformat.

## Schema Links
- FOAF http://xmlns.com/foaf/spec/
- DC http://dublincore.org/documents/2012/06/14/dcmi-terms/
- SKOS http://www.w3.org/TR/2008/WD-skos-reference-20080829/skos.html
- ORG http://www.w3.org/TR/vocab-org/

