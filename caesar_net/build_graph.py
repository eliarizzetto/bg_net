import networkx as nx
from get_relations import final_relations
import matplotlib.pyplot as plt


nodes = {name for rel in final_relations for name in rel if type(name) == str}




G = nx.Graph()

for n in nodes:
    G.add_node(n)

for item in final_relations:
    G.add_edge(item[0], item[1], weight=item[2])


# VISUALIZATION
# nx.draw(G)
# plt.show()

print(G.edges().data())
