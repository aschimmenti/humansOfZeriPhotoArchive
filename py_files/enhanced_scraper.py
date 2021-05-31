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

name_file = open('queryResults.json') 
base_url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=%s&language=en&format=json&limit=50"

data = json.load(name_file)
dict_of_results = {}
list_of_conceptualuris = []
for idx, row in enumerate(data["results"]["bindings"]):
    search_string = row["photographer_label"]["value"] 
    final_str =  ('+'.join(search_string.split(' '))).strip()
    search_res = requests.get( base_url % final_str).json()
    n_results = len(search_res['search'])
    if(n_results == 0):
        continue

    search_results = []
    search_results.extend(search_res['search'])
    
    if('search-continue' in search_res.keys()):
        any_remaining_data = True
        continue_val = 1
        while(any_remaining_data):
            new_results = requests.get((base_url + ('&continue=%i'%continue_val)) % final_str).json()
            search_results.extend(new_results['search'])
            any_remaining_data ='search-continue' in  new_results.keys()
            continue_val += 1
    for s in search_results:
            list_of_conceptualuris.append(s['concepturi'])

def suit_for_SPARQL_dinner(list_of_uris): 
    bracketed_uris = []
    for uri in list_of_uris:
        suited_uri = '<' + uri + '>'
        bracketed_uris.append(suited_uri)
    return bracketed_uris

def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

uris = ' '.join(suit_for_SPARQL_dinner(list_of_conceptualuris))

def save_to_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

save_to_file(uris, "uris.txt")
