from os import defpath
import networkx as nx
import matplotlib.pyplot as plt
import json 
from collections import defaultdict
from networkx.readwrite import json_graph
from networkx.readwrite.json_graph.node_link import node_link_data
from networkx.readwrite import json_graph;
from itertools import product

def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

G = nx.MultiGraph()
name_file = open('py_files/json_files/worklocations.json')
data = json.load(name_file)
color_map = []
graphdict = defaultdict()

for row in data["results"]["bindings"]:
    if "worklabel" in row.keys():  
        newk = row["worklabel"]["value"]
        if newk not in graphdict.keys():
            graphdict[newk] = list()

for row in data["results"]["bindings"]:
    if "worklabel" in row.keys(): 
        newv =  row['label']['value']
        city = row['worklabel']['value']
        citizenship = row['worklabel']['value']
        if city in graphdict.keys():
            graphdict[city].append(newv)
print(graphdict)

for key in graphdict: 
    G.add_node(key, vote="city")
    print(key)
    for value in graphdict[key]:
        G.add_node(value, vote="person")
        G.add_edge(key, value)
        

color_map = []
for node, data in G.nodes(data=True):
    if data['vote'] == 'city':
        color_map.append(0.25)  # blue color
    elif data['vote'] == 'person':
        color_map.append(0.7)  # yellow color

nx.draw(G, vmin=0, vmax=1, cmap=plt.cm.jet, node_color=color_map, with_labels=True)
plt.show()


    
#italian cities with >= 4 are: Rome, Bologna, Milan, Florence, Venice
higher_n_cities = defaultdict()
italian_cities = ['Rome','Bologna','Milan','Florence','Venice']
for c in italian_cities:
    higher_n_cities[c] = list()

IC = nx.MultiGraph()

for key in graphdict:  
    for key2 in higher_n_cities:
        if key == key2: 
            higher_n_cities[key2] = graphdict[key].copy()

print(higher_n_cities)

for key in higher_n_cities: 
    IC.add_node(key, vote="city")
    for value in higher_n_cities[key]:
        IC.add_node(value, vote="person")
        IC.add_edge(key, value)


color_map = []
for node, data in IC.nodes(data=True):
    if data['vote'] == 'city':
        color_map.append(0.25)  # blue color
    elif data['vote'] == 'person':
        color_map.append(0.7)  # yellow color        


nx.draw(IC, vmin=0, vmax=1, cmap=plt.cm.jet, node_color=color_map, with_labels=True)
plt.show()

#choose the city 


x = json_graph.node_link_data(IC)
afterparty_trash('smallergraph.json', x)




#name_file_dates = open('py_files/json_files/photographer_dates.json')
#dates = json.load(name_file_dates)
# def dates(list):
#    dates_list = list()
#    for row in dates["results"]["bindings"]:
#        if 'birth' and 'death' in row.keys():
#            birth = row['birth']['value'][:4]
#            photographer = row['label']['value']
#            death = row['death']['value'][:4]
#            dates_list.append((photographer, [int(birth), int(death)]))
#    print(dates_list)









#from datetime import datetime
#from collections import namedtuple
#Range = namedtuple('Range', ['start', 'end'])
#for p1, p2 in product(dates_list, dates_list):
#    if p1 != p2: 
#        r1 = Range(start=datetime(p1[1][0],1,1), end=datetime(p1[1][1],1,1))
#        r2 = Range(start=datetime(p2[1][0],1,1), end=datetime(p2[1][1],1,1))
#        latest_start = max(r1.start, r2.start)
#        earliest_end = min(r1.end, r2.end)
#        delta = (earliest_end - latest_start).days + 1
#        overlap = max(0, delta)
        #print(overlap)




