import networkx as nx
from get_relations import final_relations
import matplotlib.pyplot as plt
from networkx.algorithms import community
from pprint import pprint

nodes = {name for rel in final_relations for name in rel if type(name) == str}




G = nx.Graph()

for n in nodes:
    G.add_node(n)

for item in final_relations:
    G.add_edge(item[0], item[1], weight=item[2])


# VISUALIZATION
# nx.draw(G) # with_labels=True for showing node's label
# plt.show()

# print(G.edges().data())

degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
#
# # Get node positions
# pos = {}
# for node in G.nodes():
#     pos[node] = (degree_centrality[node], closeness_centrality[node])
#
# # Draw nodes
# nx.draw_networkx_nodes(G, pos, node_size=200, node_color=[betweenness_centrality[n] for n in G], cmap='Blues')
# nx.draw_networkx_edges(G, pos)
# plt.show()

# -------------------------------------------------------
#
# # Get the communities
# communities = community.greedy_modularity_communities(G)
#
# # Get the position of the nodes
# pos = nx.spring_layout(G)
#
# # Draw the nodes
# for c in communities:
#     nx.draw_networkx_nodes(G, pos, nodelist=c, node_size=200, node_color='blue')
# nx.draw_networkx_edges(G, pos, alpha=0.5)
#
# # Draw the other nodes
# nx.draw_networkx_nodes(G, pos, nodelist=set(G.nodes())-set().union(*communities), node_size=200, node_color='red')

# Show the plot
# plt.show()
# ----------------------------------------------------------

# for i in sorted(G.degree()):
#     print(type(i))

# pprint(sorted(G.degree, key=lambda x: x[1], reverse=True)) # print nodes ordered by degree
pprint(sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)) # print nodes ordered by their degree centrality value
pprint(sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)) # print nodes ordered by their closeness centrality value
pprint(sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)) # print nodes ordered by their betweenness centrality value
#
