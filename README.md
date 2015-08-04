# Knowledge Representation

# Dependencies

## Python 2.7.6

- ipython 3.2.1
- pymongo 3.0.2
- bson
- rdflib 4.2.0
- networkx 1.9.1
- matplotlib 1.3.1

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

__graph.py:__
Die erstellung des RDF-Graph und definitionen der Abfragefunktionen als
python Datei zur Verwendung.

__dbpedia.py:__
Definitionen der dbpedia Abfragefunkonen zur Verwendung

__ontology.ttl:__ Eigene Ontologie im Turtleformat.

# Bericht

__bericht_hodel_remus.md:__
Markdown Version vom Bericht.

__bericht_hodel_remus.pdf:__
durch Pandoc gerenderte PDF Version vom Bericht.

## Dateien zur Berichterstellung
__panbuild.sh:__
script zur PDF generierung

__titlesec.tex:__
LaTex configs für pandoc

__springer-lecture-notes-in-computer-science_modified.csl:__ 
Formatierungsdefinition der Bibliographie

__bericht.bib:__
Bibliographie in Json Format.

__images__
Ordner mit den Bilder, hat relative Beziehung zu bericht_hodel_remus.md.

__Ontology.dia:__
Dia File. Grafische darstellung der Ontologie.



## Schema Links
- FOAF http://xmlns.com/foaf/spec/
- DC http://dublincore.org/documents/2012/06/14/dcmi-terms/
- SKOS http://www.w3.org/TR/2008/WD-skos-reference-20080829/skos.html
- ORG http://www.w3.org/TR/vocab-org/

