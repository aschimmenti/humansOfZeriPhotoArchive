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
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?photographer_label (COUNT(<http://purl.org/spar/pro/holdsRoleInTime>) as ?cnt)
WHERE { 
  	?x rdf:type <http://www.essepuntato.it/2014/03/fentry/Photograph> ; 
    crm:P94i_was_created_by ?creation .
    ?creation crm:P14_carried_out_by ?photographer .
    ?photographer rdfs:label ?photographer_label
 }
GROUP BY ?photographer_label 
ORDER BY DESC(?cnt) ?photographer_label
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
