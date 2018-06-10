import matplotlib.pyplot as plt
import networkx as nx
from algorithms import rdf_parser
import pandas as pd
import numpy as np

# load data
hamster_lines = rdf_parser.load_doc()
hamster_ids, hamster_friendship = rdf_parser.collect_data(hamster_lines)
hamster_friendship_dict = rdf_parser.create_friendship(hamster_ids, hamster_friendship)

#print(hamster_friendship_dict)

def check_if_mutual_friends():
    ret_val = []
    for hamster in hamster_friendship_dict.keys():
        for friend in hamster_friendship_dict.keys():
            if hamster in hamster_friendship_dict[friend] and friend in hamster_friendship_dict[hamster]:
                ret_val.append((hamster, friend))
    return ret_val

edges = check_if_mutual_friends()

clusters = pd.read_csv('birch_clustering.csv')

all_clusters = []
cluster_labels = np.unique(clusters[['label']])
print "cluster labels"
print cluster_labels
colors = ['red', 'green', 'yellow', 'blue', 'orange']


for i in cluster_labels:
    all_clusters.append(clusters.loc[clusters['label'] == i].ix[:, 0].values.tolist())


G = nx.DiGraph()
G.add_edges_from(edges)

print  type(G.nodes())

pos = nx.spring_layout(G)

color_id = 0
for i in range(0, len(all_clusters)):
    nx.draw_networkx_nodes(G, pos, nodelist=all_clusters[i], node_color=colors[color_id], node_size=20)
    color_id += 1

nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='black', arrows=True)
plt.show()
