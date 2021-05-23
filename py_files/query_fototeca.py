import rdflib
import pprint
from rdflib import Namespace
from rdflib.namespace import DCTERMS
from rdflib.namespace import RDFS
from rdflib import URIRef, Literal
from rdflib.namespace import XSD
import numpy as np 
import matplotlib.pyplot as plt 
from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
import csv

ssl._create_default_https_context = ssl._create_unverified_context

# get the endpoint API
fototeca_endpoint = "http://data.fondazionezeri.unibo.it/sparql"

# prepare the query : 10 random triples
my_SPARQL_query = """

SELECT ?label 
WHERE <https://www.wikidata.org/wiki/Q106652385> ?a ?label



"""

# set the endpoint 
sparql_ft = SPARQLWrapper(fototeca_endpoint)
# set the query
sparql_ft.setQuery(my_SPARQL_query)
# set the returned format
sparql_ft.setReturnFormat(JSON)
# get the results
results = sparql_ft.query().convert()

# manipulate the result
for result in results["results"]["bindings"]:
    print(result["photographer"]["value"], result["cnt"]["value"])
