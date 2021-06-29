from SPARQLWrapper.Wrapper import POST
import rdflib
from rdflib import Namespace
from rdflib.namespace import DCTERMS
from rdflib.namespace import RDFS
from rdflib import URIRef, Literal
from rdflib.namespace import XSD
from SPARQLWrapper import SPARQLWrapper, JSON, GET, POST
import csv 
import pandas as pd
from json import decoder
import requests
import ssl
import json 


ssl._create_default_https_context = ssl._create_unverified_context
sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setMethod(POST)

###################################################################################

#adds the uris from a sparql query to a list, its best use is with the function below 
def invitation_list(data, string_to_match):
    invitated_uris = set()
    for result in data["results"]["bindings"]:
        invitated_uris.add(result[string_to_match]["value"]) 
        uris = list(invitated_uris)
    return uris

#once you have the list you can: 
#clean the list (first below)
#suit the uris with the brackets (second below)
#takes a list of uris from a query and adds brackets for a sparql query 

def suit_for_SPARQL_dinner(list_of_uris): 
    bracketed_uris = []
    for uri in list_of_uris:
        suited_uri = '<' + uri + '>'
        bracketed_uris.append(suited_uri)
    return bracketed_uris

#if you need to remove uris from a list, it's a basic linear search 
def remove_uninvited_guests_from_list(uninvited_guests, invitation_list):
    final_set = set()
    if len(invitation_list) < 2: 
        return None
    for person in uninvited_guests: 
        for i in range(len(invitation_list)):
            if (person == invitation_list[i]): 
                print('got out')
                print(person)
            else: 
                final_set.add(invitation_list[i])
    exclusive_list = list(final_set) 
    return exclusive_list

def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)
##################################################################################

name_file = open('py_files/json_files/final_photographer_Q5.json')
data = json.load(name_file)
uris = suit_for_SPARQL_dinner(invitation_list(data, "photographer"))
string_uris = ' '.join(uris)

#first query: find out if there's some group of people that isn't a Q5 themselves
#if there's someone, check if there's some people related to them and update the list of uris

if_entity = """select ?otherpeople ?photographer
where {VALUES  ?photographer  {"""+string_uris+"""}
    ?photographer wdt:P31 ?o .
    FILTER(?o != wd:Q5) . 
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  
    ?photographer ?property ?otherpeople .
    ?otherpeople wdt:P31 wd:Q5 .
}

GROUP BY ?otherpeople ?photographer"""

sparql.setQuery(if_entity)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print(results)
#now add to the uris the list of new uris, first make a list of them, then 'suit them' with the brackets
uris.extend(suit_for_SPARQL_dinner(invitation_list(results, "otherpeople")))
#create a second list out of the other output, and have a list of the people to remove from the now unpacked list
people_out = suit_for_SPARQL_dinner(invitation_list(results, 'photographer'))
#use the two previous lists 
new_uris = remove_uninvited_guests_from_list(people_out, uris)
new_string_uris = ' '.join(new_uris)
##############################################
print(new_string_uris)

#now let's see the citizenships of the new uris selected
citizenships_query= """
select ?photographer ?label (group_concat(?citizenship) as ?citizenships) ?worklocation
where {VALUES ?photographer {""" + new_string_uris + """}
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  
       optional {
          ?photographer wdt:P27 ?citizenship
}
}
group by ?photographer ?label
"""
sparql.setQuery(citizenships_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
afterparty_trash('py_files/json_files/worklocation_birth.json', results)

#let's check the dates related to the new uris 


collections= """
select ?photographer ?label (group_concat(distinct ?institution;separator="; ") as ?institutions)
where {VALUES ?photographer {""" + new_string_uris + """}
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  
    ?photographer wdt:P6379 ?institutions
}
group by ?photographer ?label
"""
sparql.setQuery(collections)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
afterparty_trash('py_files/json_files/collections.json', results)

