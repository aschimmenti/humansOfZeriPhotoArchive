from SPARQLWrapper.Wrapper import CSV, POST
import rdflib
from rdflib import Namespace
from rdflib.namespace import DCTERMS
from rdflib.namespace import RDFS
from rdflib import URIRef, Literal
from rdflib.namespace import XSD
from SPARQLWrapper import SPARQLWrapper, JSON, GET, POST, CSV
import csv 
import pandas as pd
from json import decoder
import requests
import ssl
import json 

new_string_uris = """<http://www.wikidata.org/entity/Q18934975> <http://www.wikidata.org/entity/Q61482172> <http://www.wikidata.org/entity/Q75379946> <http://www.wikidata.org/entity/Q21176613> <http://www.wikidata.org/entity/Q16632909> <http://www.wikidata.org/entity/Q102281430> <http://www.wikidata.org/entity/Q3723011> <http://www.wikidata.org/entity/Q102281190> <http://www.wikidata.org/entity/Q58242413> <http://www.wikidata.org/entity/Q102281349> <http://www.wikidata.org/entity/Q59743982> <http://www.wikidata.org/entity/Q102075978> <http://www.wikidata.org/entity/Q647812> <http://www.wikidata.org/entity/Q3840227> <http://www.wikidata.org/entity/Q18509122> <http://www.wikidata.org/entity/Q106417607> <http://www.wikidata.org/entity/Q24239722> <http://www.wikidata.org/entity/Q3160907> <http://www.wikidata.org/entity/Q5813202> <http://www.wikidata.org/entity/Q84594380> <http://www.wikidata.org/entity/Q106652385> <http://www.wikidata.org/entity/Q346323> <http://www.wikidata.org/entity/Q48444861> <http://www.wikidata.org/entity/Q95133787> <http://www.wikidata.org/entity/Q97940625> <http://www.wikidata.org/entity/Q102282921> <http://www.wikidata.org/entity/Q946185> <http://www.wikidata.org/entity/Q106650664> <http://www.wikidata.org/entity/Q2346257> <http://www.wikidata.org/entity/Q365683> <http://www.wikidata.org/entity/Q3109003> <http://www.wikidata.org/entity/Q102282749> <http://www.wikidata.org/entity/Q2425872> <http://www.wikidata.org/entity/Q61476278> <http://www.wikidata.org/entity/Q103135077> <http://www.wikidata.org/entity/Q105986035> <http://www.wikidata.org/entity/Q55053644> <http://www.wikidata.org/entity/Q61992274> <http://www.wikidata.org/entity/Q30127547> <http://www.wikidata.org/entity/Q18508704> <http://www.wikidata.org/entity/Q64212> <http://www.wikidata.org/entity/Q3441292> <http://www.wikidata.org/entity/Q18716069> <http://www.wikidata.org/entity/Q23560875> <http://www.wikidata.org/entity/Q21542680> <http://www.wikidata.org/entity/Q3750053> <http://www.wikidata.org/entity/Q449754> <http://www.wikidata.org/entity/Q102281528> <http://www.wikidata.org/entity/Q3724533> <http://www.wikidata.org/entity/Q59575316> <http://www.wikidata.org/entity/Q17132342> <http://www.wikidata.org/entity/Q55679892> <http://www.wikidata.org/entity/Q155158> <http://www.wikidata.org/entity/Q1445526> <http://www.wikidata.org/entity/Q60241073> <http://www.wikidata.org/entity/Q86137496> 
<http://www.wikidata.org/entity/Q18508633> <http://www.wikidata.org/entity/Q67294703> <http://www.wikidata.org/entity/Q110373> <http://www.wikidata.org/entity/Q585323> <http://www.wikidata.org/entity/Q3034711> <http://www.wikidata.org/entity/Q3831697> 
<http://www.wikidata.org/entity/Q43128341> <http://www.wikidata.org/entity/Q200890> <http://www.wikidata.org/entity/Q52156353> <http://www.wikidata.org/entity/Q252357> <http://www.wikidata.org/entity/Q102282957> <http://www.wikidata.org/entity/Q102281354> <http://www.wikidata.org/entity/Q17426655> <http://www.wikidata.org/entity/Q17350272> <http://www.wikidata.org/entity/Q86736457> <http://www.wikidata.org/entity/Q3157912> <http://www.wikidata.org/entity/Q215618> <http://www.wikidata.org/entity/Q62572993> <http://www.wikidata.org/entity/Q100138863> <http://www.wikidata.org/entity/Q789672> <http://www.wikidata.org/entity/Q12025975> <http://www.wikidata.org/entity/Q106650408> <http://www.wikidata.org/entity/Q378129> <http://www.wikidata.org/entity/Q6187840> <http://www.wikidata.org/entity/Q16164590> <http://www.wikidata.org/entity/Q18811896> <http://www.wikidata.org/entity/Q5660348> <http://www.wikidata.org/entity/Q106936993> <http://www.wikidata.org/entity/Q16867239> <http://www.wikidata.org/entity/Q51883685> <http://www.wikidata.org/entity/Q26242203> <http://www.wikidata.org/entity/Q25939348> <http://www.wikidata.org/entity/Q1676501> <http://www.wikidata.org/entity/Q22113142> <http://www.wikidata.org/entity/Q18169099> <http://www.wikidata.org/entity/Q2412846> <http://www.wikidata.org/entity/Q3081037> <http://www.wikidata.org/entity/Q106653081> <http://www.wikidata.org/entity/Q16622457> <http://www.wikidata.org/entity/Q3131559> <http://www.wikidata.org/entity/Q60236397>"""

ssl._create_default_https_context = ssl._create_unverified_context
sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
sparql.setMethod(POST)

collections= """
select ?photographer ?label (group_concat(?institution_label;separator="; ") as ?institutions_label) 
where {VALUES ?photographer {"""+new_string_uris+"""}
    ?photographer rdfs:label ?label .
    FILTER(LANG(?label) = "en").  
    ?photographer wdt:P6379 ?institution .
    ?institution rdfs:label ?institution_label
    FILTER(LANG(?institution_label) = "en").  

}
group by ?photographer ?label ?instutions_label
"""

sparql.setQuery(collections)
sparql.setReturnFormat(CSV)
results = sparql.query().convert()
print(results)

df = pd.read_csv('py_files/collections.csv') 
df.to_csv('py_files/collections.csv')

