import rdflib
from rdflib import Namespace
from rdflib.namespace import DCTERMS
from rdflib.namespace import RDFS
from rdflib import URIRef, Literal
from rdflib.namespace import XSD
from SPARQLWrapper import SPARQLWrapper, JSON, GET
import csv 
import pandas as pd
from json import decoder
import requests
import ssl
import json 
ssl._create_default_https_context = ssl._create_unverified_context

name_file = open('py_files\photographers_IDs.json')
data = json.load(name_file)

def suit_for_SPARQL_dinner(list_of_uris): 
    bracketed_uris = []
    for uri in list_of_uris:
        suited_uri = '<' + uri + '>'
        bracketed_uris.append(suited_uri)
    return bracketed_uris

def invitation_list(data, string_to_match):
    invitated_uris = list()
    for result in data["results"]["bindings"]:
        invitated_uris.append(result[string_to_match]["value"]) 
    return invitated_uris

uris = ' '.join(suit_for_SPARQL_dinner(invitation_list(data, "photographerEntity")))  

sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setMethod(GET)

my_SPARQL_query= """
select ?photographer ?label (group_concat(?citizenship) as ?citizenships)
where {VALUES ?photographer {""" + uris + """}
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  

       optional {
          ?photographer wdt:P27 ?citizenship
}
}
group by ?photographer ?label
"""
sparql.setQuery(my_SPARQL_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

with open('citizenships.json', 'w') as outfile:
    json.dump(results, outfile)

my_dates_query = """select ?photographer ?label ?birth ?death
where {VALUES ?photographer {"""+uris+"""}   ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  

       optional {
          ?photographer wdt:P569 ?birth ; wdt:P570 ?death
}
}
group by ?photographer ?label ?birth ?death"""

sparql.setQuery(my_dates_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

with open('birthdeathdates.json', 'w') as outfile:
    json.dump(results, outfile)


my_worklocation_query = """select ?photographer ?label ?worklabel
where {VALUES ?photographer {"""+uris+"""} .
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  

       optional {
          ?photographer wdt:P937 ?worklocation .
          ?worklocation rdfs:label ?worklabel
          FILTER(LANG(?worklabel) = "en").  

}
}
group by ?photographer ?label ?worklabel"""

sparql.setQuery(my_worklocation_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

with open('worklocations.json', 'w') as outfile:
    json.dump(results, outfile)
