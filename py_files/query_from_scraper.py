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

my_SPARQL_query= """
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?photographer ?label 
WHERE {
    VALUES ?photographer {""" + uris + """} .
    ?photographer ?p ?o .
    FILTER (?p = wdt:P106 || ?p = wdt:P31) .
    FILTER (?o = wd:Q33231 || ?o = wd:Q672070 || ?o = wd:Q18224771 ) .
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").
    }
GROUP BY ?photographer ?label 
"""


# set the endpoint 
# set the query
sparql.setQuery(my_SPARQL_query)
sparql.setMethod(POST)
# set the returned format
sparql.setReturnFormat(JSON)
# get the results
results = sparql.query().convert()
afterparty_trash("phot_ids.json", results)

