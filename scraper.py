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
import wptools
import json
import wikipedia 

ssl._create_default_https_context = ssl._create_unverified_context

wikidata_endpoint = 'https://query.wikidata.org/'
# Opening JSON file
f = open('queryResults.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)	

#page = wptools.page
#page.get_query()

list_of_labels = []
for row in data["results"]["bindings"]:
	list_of_labels.append(row["photographer_label"]["value"])
	
founds = []
for x in list_of_labels:
    try:
        page = wptools.page(x)
        page.get_query()
        y = page.data['wikidata_url']
        founds.append(y) 
    except LookupError:
        print("got exception")
print(founds)
    