import rdflib
from rdflib import Namespace
from rdflib import URIRef

g=rdflib.Graph()
filename = r'./artist.owl'
g.load(filename, format='xml')

print g.serialize(format='pretty-xml')