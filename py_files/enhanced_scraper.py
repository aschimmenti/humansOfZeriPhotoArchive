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
#do not use
def to_text(path):
    final_text = list()
    with open(path, newline='') as csvfile:
        photographers = csv.DictReader(csvfile)
        for row in photographers:
            x = str(row['photographer']) 
            y = int(row['contribution count'])
            text = list()
            for n in range(y):
                text.append(x)
            final_text.append(' '.join(text))
    final_string = ' '.join(final_text)
    return final_string
        
def save_to_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

def reverse_string(string): 
    comma = ', '
    string_to_join = ''
    if comma in string: 
        x = string.split(", ")
        string_to_join = str(x[1]) + ' '+ str(x[0])
        return string_to_join
    else: 
        return string

name_file = open('fototeca_photographers.json') 
base_url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=%s&language=en&format=json&limit=50"

data = json.load(name_file)
dict_of_results = {}
list_of_conceptualuris = []

for idx, row in enumerate(data["results"]["bindings"]):
    search_string = row["photographer_label"]["value"]
    search_string = reverse_string(search_string)
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


uris = ' '.join(suit_for_SPARQL_dinner(list_of_conceptualuris))

def save_to_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

save_to_file(uris, "uris3.txt")

