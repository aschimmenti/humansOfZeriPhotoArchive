import networkx as nx
import matplotlib as plt
import json 

G = nx.Graph()
name_file = open('./worklocations.json')
data = json.load(name_file)

graphdict = dict()

for row in data["results"]["bindings"]:
    if "worklabel" in row.keys(): 
        newk = row["worklabel"]["value"]
        graphdict[newk] = list()

for row in data["results"]["bindings"]:
    if "worklabel" in row.keys(): 
        newvalue = row["photographer"]["value"]
        #if in photographer = city and city == dict.keys 
        #append photographer to city 
        