import networkx as nx
import matplotlib.pyplot as plt
import json 
from collections import defaultdict
from networkx.readwrite import json_graph
from networkx.readwrite.json_graph.node_link import node_link_data
from networkx.readwrite import json_graph;


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


#nx.draw(G, vmin=0, vmax=1, cmap=plt.cm.jet, node_color=color_map, with_labels=True)
#plt.show()

#with open('graph.json', 'w') as outfile:
    #json.dump(json_graph.node_link_data(G))

x = json_graph.node_link_data(G)
afterparty_trash('graph.json', x)