import matplotlib.pyplot as plt
import networkx as nx
import math

n = 150
m = 4
graph = nx.barabasi_albert_graph(n, m)

pos = nx.nx.spring_layout(graph,iterations=20)
nx.draw_networkx(graph, node_size = [math.pow(graph.degree(v),2) for v in graph])
labels = {i: i + 1 for i in graph.nodes()}
# nx.draw_networkx_labels(graph, pos, labels, font_size=15)
plt.show()

