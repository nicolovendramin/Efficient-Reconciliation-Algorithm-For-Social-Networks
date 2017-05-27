import matplotlib.pyplot as plt
import networkx as nx
import math
import os
import random

s_one = 0.1
s_two = 0.3
n = 150
m = 4
graph = nx.barabasi_albert_graph(n, m)

pos = nx.nx.spring_layout(graph,iterations=20)
plt.figure(1)
nx.draw_networkx(graph, node_size = [math.pow(graph.degree(v),2) for v in graph])
labels = {i: i + 1 for i in graph.nodes()}

social_one = graph.copy()
social_two = graph.copy()

for e in graph.edges_iter():
    keep_one = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    keep_two = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    if keep_one < s_one:
        social_one.remove_edge(e[0], e[1])
    if keep_two < s_two:
        social_two.remove_edge(e[0], e[1])

plt.figure(2)
nx.draw_networkx(social_one, node_size = [math.pow(graph.degree(v),2) for v in graph], node_color = 'b')

plt.figure(3)
nx.draw_networkx(social_two, node_size = [math.pow(graph.degree(v),2) for v in graph], node_color = 'g')

nodes_real = graph.nodes()
nodes_one = social_one.nodes()
nodes_two = social_two.nodes()

print(nodes_one,nodes_real,nodes_two)
tot_degree_real = 0
tot_degree_one = 0
tot_degree_two = 0

for i in nodes_real:
    if i not in nodes_one or i not in nodes_two:
        print("Graph reduction error")
    tot_degree_one += social_one.degree(i)
    tot_degree_real += graph.degree(i)
    tot_degree_two += social_two.degree(i)

print(tot_degree_real, tot_degree_one, tot_degree_two)

plt.show()
