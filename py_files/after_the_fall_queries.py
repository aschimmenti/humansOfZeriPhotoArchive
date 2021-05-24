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
sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setMethod(GET)


###################################################################################

#adds the uris from a sparql query to a list, its best use is with the function below 
def invitation_list(data, string_to_match):
    invitated_uris = list()
    for result in data["results"]["bindings"]:
        invitated_uris.append(result[string_to_match]["value"]) 
    return invitated_uris

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
    exclusive_list = []
    if len(invitation_list) < 2: 
        return None
    for person in uninvited_guests: 
        for i in range(len(invitation_list)):
            if (person == invitation_list[i]): 
                print('got out')
            else: 
                exclusive_list.append(invitation_list[i])
    return exclusive_list

def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)
##################################################################################

name_file = open('py_files\photographers_IDs.json')
data = json.load(name_file)
uris = suit_for_SPARQL_dinner(invitation_list(data, "photographerEntity"))
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
#results = sparql.query().convert()


#now add to the uris the list of new uris, first make a list of them, then 'suit them' with the brackets
#uris.extend(suit_for_SPARQL_dinner(invitation_list(results, "otherpeople")))
#create a second list out of the other output, and have a list of the people to remove from the now unpacked list
#people_out = suit_for_SPARQL_dinner(invitation_list(results, 'photographer'))
#use the two previous lists 
people_out = ['<http://www.wikidata.org/entity/Q644689>']
uris = ['<http://www.wikidata.org/entity/Q3157912>', '<http://www.wikidata.org/entity/Q3160907>', '<http://www.wikidata.org/entity/Q3441292>', '<http://www.wikidata.org/entity/Q3840227>', '<http://www.wikidata.org/entity/Q106936993>', '<http://www.wikidata.org/entity/Q106652385>', '<http://www.wikidata.org/entity/Q449754>', '<http://www.wikidata.org/entity/Q644689>', '<http://www.wikidata.org/entity/Q647812>', '<http://www.wikidata.org/entity/Q2346257>', '<http://www.wikidata.org/entity/Q2412846>', '<http://www.wikidata.org/entity/Q30093317>', '<http://www.wikidata.org/entity/Q52155339>', '<http://www.wikidata.org/entity/Q58242413>', '<http://www.wikidata.org/entity/Q59743982>', '<http://www.wikidata.org/entity/Q61992274>', '<http://www.wikidata.org/entity/Q67294703>', '<http://www.wikidata.org/entity/Q100138863>', '<http://www.wikidata.org/entity/Q102280734>', '<http://www.wikidata.org/entity/Q106650408>', '<http://www.wikidata.org/entity/Q155158>', '<http://www.wikidata.org/entity/Q365683>', '<http://www.wikidata.org/entity/Q3081037>', '<http://www.wikidata.org/entity/Q25939348>', '<http://www.wikidata.org/entity/Q30127547>', '<http://www.wikidata.org/entity/Q94869574>', '<http://www.wikidata.org/entity/Q102282957>', '<http://www.wikidata.org/entity/Q16164590>', '<http://www.wikidata.org/entity/Q18508633>', '<http://www.wikidata.org/entity/Q18934975>']
new_uris = remove_uninvited_guests_from_list(people_out, uris)
new_string_uris = ' '.join(new_uris)
##############################################
print(new_string_uris)

#now let's see the citizenships of the new uris selected
citizenships_query= """
select ?photographer ?label (group_concat(?citizenship) as ?citizenships)
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
afterparty_trash('citizenships.json', results)

#let's check the dates related to the new uris 

dates_query = """select ?photographer ?label ?birth ?death
where {VALUES ?photographer {"""+new_string_uris+"""}   ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  
       optional {
          ?photographer wdt:P569 ?birth ; wdt:P570 ?death
}
}
group by ?photographer ?label ?birth ?death"""
sparql.setQuery(dates_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
afterparty_trash('birthdeathdates.json', results)

#now let's see the work places of the new uris 
worklocation_query = """select ?photographer ?label ?worklabel
where {VALUES ?photographer {"""+new_string_uris+"""} .
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  
       optional {
          ?photographer wdt:P937 ?worklocation .
          ?worklocation rdfs:label ?worklabel
          FILTER(LANG(?worklabel) = "en").  
}
}
group by ?photographer ?label ?worklabel"""
sparql.setQuery(worklocation_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
afterparty_trash('worklocations.json', results)


total_query ="""select ?photographer ?label (group_concat(?citizenship) as ?citizenships) ?birth ?death (group_concat(?worklocation) as ?worklocations)
where {VALUES  ?photographer  {<http://www.wikidata.org/entity/Q3157912> <http://www.wikidata.org/entity/Q3160907> <http://www.wikidata.org/entity/Q3441292> 
<http://www.wikidata.org/entity/Q3840227> <http://www.wikidata.org/entity/Q106936993> <http://www.wikidata.org/entity/Q106652385> <http://www.wikidata.org/entity/Q449754> <http://www.wikidata.org/entity/Q647812> <http://www.wikidata.org/entity/Q2346257> <http://www.wikidata.org/entity/Q2412846> <http://www.wikidata.org/entity/Q30093317> <http://www.wikidata.org/entity/Q52155339> <http://www.wikidata.org/entity/Q58242413> <http://www.wikidata.org/entity/Q59743982> <http://www.wikidata.org/entity/Q61992274> <http://www.wikidata.org/entity/Q67294703> <http://www.wikidata.org/entity/Q100138863> <http://www.wikidata.org/entity/Q102280734> <http://www.wikidata.org/entity/Q106650408> <http://www.wikidata.org/entity/Q155158> <http://www.wikidata.org/entity/Q365683> <http://www.wikidata.org/entity/Q3081037> <http://www.wikidata.org/entity/Q25939348> <http://www.wikidata.org/entity/Q30127547> <http://www.wikidata.org/entity/Q94869574> <http://www.wikidata.org/entity/Q102282957> <http://www.wikidata.org/entity/Q16164590> <http://www.wikidata.org/entity/Q18508633> <http://www.wikidata.org/entity/Q18934975>}.
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  
       OPTIONAL {
          ?photographer wdt:P27 ?citizenship . 
          ?photographer wdt:P937 ?worklocation .
          ?worklocation rdfs:label ?worklabel .
          FILTER(LANG(?worklabel) = "en").  
          ?photographer wdt:P569 ?birth }.
       OPTIONAL {
          ?photographer wdt:P570 ?death }.
}
group by ?photographer ?label ?birth ?death """
