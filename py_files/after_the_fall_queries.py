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

name_file = open('./final_photographer_Q5.json')
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
#afterparty_trash('birthdeathdates.json', results)

#now let's see the work places of the new uris 
worklocation_query = """select DISTINCT ?photographer ?label ?worklabel
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


total_query ="""select ?photographer ?label ?birth ?death  (group_concat(?worklabel) as ?worklabels)
where {VALUES  ?photographer  {"""+new_string_uris+"""}
    FILTER(LANG(?label) = "en").  
        OPTIONAL {   
         ?photographer wdt:P937 ?worklocation .
          ?worklocation rdfs:label ?worklabel .
          FILTER(LANG(?worklabel) = "en") }.
        OPTIONAL {
          ?photographer wdt:P569 ?birth }.
        OPTIONAL {
          ?photographer wdt:P570 ?death }.
}
       
group by ?photographer ?label ?birth ?death ?worklabels"""
sparql.setQuery(total_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
afterparty_trash('total_query.json', results)


"""select ?photographer ?label ?birth ?death  (group_concat(?worklabel) as ?worklabels)
where {VALUES  ?photographer  {<http://www.wikidata.org/entity/Q102282749> <http://www.wikidata.org/entity/Q106650408> <http://www.wikidata.org/entity/Q59575316> <http://www.wikidata.org/entity/Q215618> <http://www.wikidata.org/entity/Q3750053> <http://www.wikidata.org/entity/Q18509122> <http://www.wikidata.org/entity/Q17132342> <http://www.wikidata.org/entity/Q3724533> <http://www.wikidata.org/entity/Q97940625> <http://www.wikidata.org/entity/Q102281528> <http://www.wikidata.org/entity/Q1676501> <http://www.wikidata.org/entity/Q64212> <http://www.wikidata.org/entity/Q3081037> <http://www.wikidata.org/entity/Q52156353> <http://www.wikidata.org/entity/Q58242413> <http://www.wikidata.org/entity/Q2045337> <http://www.wikidata.org/entity/Q18934975> <http://www.wikidata.org/entity/Q106417607> <http://www.wikidata.org/entity/Q155158> <http://www.wikidata.org/entity/Q18169099> <http://www.wikidata.org/entity/Q102281354> <http://www.wikidata.org/entity/Q585323> <http://www.wikidata.org/entity/Q24239722> <http://www.wikidata.org/entity/Q789672> <http://www.wikidata.org/entity/Q102281430> <http://www.wikidata.org/entity/Q2346257> <http://www.wikidata.org/entity/Q3441292> <http://www.wikidata.org/entity/Q23560875> <http://www.wikidata.org/entity/Q12025975> <http://www.wikidata.org/entity/Q86137496> <http://www.wikidata.org/entity/Q85724045> <http://www.wikidata.org/entity/Q378129> <http://www.wikidata.org/entity/Q102282957> <http://www.wikidata.org/entity/Q106936993> <http://www.wikidata.org/entity/Q30308695> <http://www.wikidata.org/entity/Q102282921> <http://www.wikidata.org/entity/Q107030756> <http://www.wikidata.org/entity/Q106653081> <http://www.wikidata.org/entity/Q3831697> <http://www.wikidata.org/entity/Q110373> <http://www.wikidata.org/entity/Q3160907> <http://www.wikidata.org/entity/Q67294703> <http://www.wikidata.org/entity/Q21176613> <http://www.wikidata.org/entity/Q61482172> <http://www.wikidata.org/entity/Q30308623> <http://www.wikidata.org/entity/Q644689> <http://www.wikidata.org/entity/Q200890> <http://www.wikidata.org/entity/Q449754> <http://www.wikidata.org/entity/Q18811896> <http://www.wikidata.org/entity/Q3109003> <http://www.wikidata.org/entity/Q18716069> <http://www.wikidata.org/entity/Q3034711> <http://www.wikidata.org/entity/Q84594380> <http://www.wikidata.org/entity/Q16632909> <http://www.wikidata.org/entity/Q5660348> <http://www.wikidata.org/entity/Q3723011> <http://www.wikidata.org/entity/Q100138863> <http://www.wikidata.org/entity/Q18508633> <http://www.wikidata.org/entity/Q17426655> <http://www.wikidata.org/entity/Q61992274> <http://www.wikidata.org/entity/Q30127547> <http://www.wikidata.org/entity/Q16622457> <http://www.wikidata.org/entity/Q106650664> <http://www.wikidata.org/entity/Q16867239> <http://www.wikidata.org/entity/Q86736457> <http://www.wikidata.org/entity/Q346323> <http://www.wikidata.org/entity/Q16164590> <http://www.wikidata.org/entity/Q85859399> <http://www.wikidata.org/entity/Q59743982> <http://www.wikidata.org/entity/Q55679892> <http://www.wikidata.org/entity/Q647812> <http://www.wikidata.org/entity/Q21542680> <http://www.wikidata.org/entity/Q60241073> <http://www.wikidata.org/entity/Q30308759> <http://www.wikidata.org/entity/Q5813202> <http://www.wikidata.org/entity/Q6187840> <http://www.wikidata.org/entity/Q48444861> <http://www.wikidata.org/entity/Q17350272> <http://www.wikidata.org/entity/Q102281190> <http://www.wikidata.org/entity/Q22113142> <http://www.wikidata.org/entity/Q102281349> <http://www.wikidata.org/entity/Q61476278> <http://www.wikidata.org/entity/Q18508704> <http://www.wikidata.org/entity/Q102280849> <http://www.wikidata.org/entity/Q60236397> <http://www.wikidata.org/entity/Q26242203> <http://www.wikidata.org/entity/Q103135077> <http://www.wikidata.org/entity/Q106652385> <http://www.wikidata.org/entity/Q62572993> <http://www.wikidata.org/entity/Q75379946> <http://www.wikidata.org/entity/Q2412846> <http://www.wikidata.org/entity/Q946185> <http://www.wikidata.org/entity/Q51883685> <http://www.wikidata.org/entity/Q1445526> <http://www.wikidata.org/entity/Q43128341> <http://www.wikidata.org/entity/Q102075978> <http://www.wikidata.org/entity/Q25939348> <http://www.wikidata.org/entity/Q3131559> <http://www.wikidata.org/entity/Q3157912> <http://www.wikidata.org/entity/Q252357> <http://www.wikidata.org/entity/Q2425872> <http://www.wikidata.org/entity/Q95133787> <http://www.wikidata.org/entity/Q3840227> <http://www.wikidata.org/entity/Q105986035>}    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  
       OPTIONAL {   
         ?photographer wdt:P937 ?worklocation .
          ?worklocation rdfs:label ?worklabel .
          FILTER(LANG(?worklabel) = "en") }.
        OPTIONAL {
          ?photographer wdt:P569 ?birth }.
       OPTIONAL {
          ?photographer wdt:P570 ?death }.
}
       
group by ?photographer ?label ?birth ?death ?worklabels"""



