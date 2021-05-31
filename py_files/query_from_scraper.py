from json import decoder
from SPARQLWrapper.Wrapper import GET
import requests
import json
import rdflib
import pprint
from rdflib import Namespace
from rdflib.namespace import DCTERMS
from rdflib.namespace import RDFS
from rdflib import URIRef, Literal
from rdflib.namespace import XSD
import numpy as np 
import matplotlib.pyplot as plt 
from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, JSON
from SPARQLWrapper import POST 
import ssl
import csv

ssl._create_default_https_context = ssl._create_unverified_context

sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setMethod(POST)

with open ("uris.txt", "r") as myfile:
    uris = myfile.readlines()
    uris = ' '.join(uris)
    
my_SPARQL_query= """
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?photographer ?label 
WHERE {
    VALUES ?photographer {""" + uris + """} .
    ?photographer wdt:P106 wd:Q33231 .
    ?photographer ?p wd:Q5 .
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").
    }
GROUP BY ?photographer ?label 
"""

def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)
        
# set the endpoint 
# set the query
sparql.setQuery(my_SPARQL_query)
sparql.setMethod(POST)
# set the returned format
sparql.setReturnFormat(JSON)
# get the results
results = sparql.query().convert()
afterparty_trash("phot_ids.json", results)

