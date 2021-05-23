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
from archerror_handling import handle_request



ssl._create_default_https_context = ssl._create_unverified_context

name_file = open('py_files/queryResults.json') 
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
conceptual_uris = []

def suit_for_SPARQL_dinner(list_of_uris): 
    bracketed_uris = []
    for uri in list_of_uris:
        suited_uri = '<' + uri + '>'
        bracketed_uris.append(suited_uri)
    return bracketed_uris


uris = ' '.join(suit_for_SPARQL_dinner(conceptual_uris))

print(uris)

sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setMethod(POST)

my_SPARQL_query= """
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?photographer ?label ?citizenships ?placeOfBirth ?worklocation
WHERE {
    VALUES ?photographer {""" + uris + """} .
    ?photographer wdt:P106 wd:Q33231 . 
    ?photographer rdfs:label ?label .
    ?photographer wdt:P31 wd:Q5 .
  OPTIONAL {
    ?photographer wdt:P27* ?citizenships .
    ?photographer wdt:P19* ?placeOfBirth . 
    ?photographer wdt:P937* ?worklocation .
    }
    FILTER(LANG(?label) = "en").
    }
GROUP BY ?photographer ?label ?citizenships ?placeOfBirth ?worklocation
LIMIT 20
"""


# set the endpoint 
# set the query
sparql.setQuery(my_SPARQL_query)
# set the returned format
sparql.setReturnFormat(JSON)
# get the results
results = sparql.query().convert()
json.dump(results) 
print(results)

for result in results["results"]["bindings"]:
    print(result["photographer"]["value"], result["label"]["value"], result["citizenship"]["value"], result["placeOfBirth"]["value"], result["worklocation"]["value"])

handle_request("https://query.wikidata.org/bigdata/namespace/wdq/sparql")