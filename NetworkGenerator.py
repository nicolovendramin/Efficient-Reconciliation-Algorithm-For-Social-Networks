import matplotlib.pyplot as plt
import networkx as nx
import math
import os

# probability that a generic node belongs to the group of the trusted identified connections
l = 0.01
# probability to keep an edge in the first social
s_one = 0.1
# probability to keep an edge in the second social
s_two = 0.3
# number of edges of our network
n = 150
# m parameter for the Preferential Attachment method
m = 4
# Graph variable representing the real underlying network
graph = nx.barabasi_albert_graph(n, m)

# Plotting instructions for the graph
# pos = nx.nx.spring_layout(graph,iterations=20)
plt.figure(1)
nx.draw_networkx(graph, node_size = [math.pow(graph.degree(v),2) for v in graph])
labels = {i: i + 1 for i in graph.nodes()}

# Copies the real network in two new variables
social_one = graph.copy()
social_two = graph.copy()

# with random independent probabilities we filter the real network to get the new partial ones
for e in graph.edges_iter():
    keep_one = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    keep_two = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    if keep_one > s_one:
        social_one.remove_edge(e[0], e[1])
    if keep_two > s_two:
        social_two.remove_edge(e[0], e[1])

# plotting instructions
plt.figure(2)
nx.draw_networkx(social_one, node_size = [math.pow(graph.degree(v),2) for v in graph], node_color = 'b')

plt.figure(3)
nx.draw_networkx(social_two, node_size = [math.pow(graph.degree(v),2) for v in graph], node_color = 'g')

# counting the total degree to assess the increased sparsity of the derived networks, selection of the trusted link set
nodes_real = graph.nodes()
nodes_one = social_one.nodes()
nodes_two = social_two.nodes()
print(nodes_one,nodes_real,nodes_two)
tot_degree_real = 0
tot_degree_one = 0
tot_degree_two = 0
identified_connections = []

for i in nodes_real:
    if i not in nodes_one or i not in nodes_two:
        print("Graph reduction error")
    tot_degree_one += social_one.degree(i)
    tot_degree_real += graph.degree(i)
    tot_degree_two += social_two.degree(i)
    link_known = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    if link_known < l:
        identified_connections.append(i)

# Printing and plotting
print(tot_degree_real, tot_degree_one, tot_degree_two)
print(identified_connections)
plt.show()
