import numpy as np
import pandas as pd
import string
import networkx as nx
import matplotlib.pyplot as plt
import json 
from networkx.readwrite.json_graph.node_link import node_link_data
from networkx.readwrite import json_graph;

df = pd.read_csv('py_files/json_files/workbirths.csv', sep=',')
df['birth'] = pd.to_datetime(df['birth'])
df['year'] = df['birth'].dt.year
lbls = df['worklabels'].values
df['worklabels'] = [lbl.split(',') for lbl in lbls]

def extract_network(df, min_year, n_years):
    x = df[df.year >= min_year]
    x = x[x.year < min_year + n_years]
    net = nx.Graph() 
    for _, row1 in x.iterrows():
        z1 = row1.label
        cities1 = row1.worklabels
        for _, row2 in x.iterrows():
            z2 = row2.label
            net.add_node(z2)
            if(z1 != z2):
                cities2 = row2.worklabels
                res = list(np.intersect1d(cities1,cities2))
                if(len(res)>0):
                    net.add_edge(z1,z2,label=res)
    return net


def afterparty_trash(filename, data_to_write):
    with open(filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

networks = []
starting_years = (1800, 1830, 1860, 1890, 1920, 1950, 1980)
window_sz = 40
counter = 0
for s_year in starting_years:
    net = extract_network(df, s_year, window_sz)
    networks.append(net)
    conn_comps = nx.connected_components(net)
    for people in conn_comps:
        if(len(people)>1):
            S = net.subgraph(people).copy()
            nx.draw(S, with_labels=True)
            plt.show()