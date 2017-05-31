import matplotlib.pyplot as plt
import networkx as nx
import math
import os

class NetworkGenerator(object):
    # probability that a generic node belongs to the group of the trusted identified connections
    l = 0.01
    # probability to keep an edge in the first social
    s_one = 0.1
    # probability to keep an edge in the second social
    s_two = 0.3
    # number of edges of our network
    n = 65000
    # m parameter for the Preferential Attachment method
    m = 40
    # Graph variable representing the real underlying network
    graph = []
    social_one = []
    social_two = []
    identified_connections = []
    d_graph = 0
    d_one = 0
    d_two = 0
    tot_degree_real = 0
    tot_degree_one = 0
    tot_degree_two = 0

    def __init__(self):
        print("Network generator initialized. To change the default configuration use the method "
              "set_parameters, to generate the networks use generate, to plot use plot_all")

    def plot_all(self):
        # Plotting instructions for the graph
        a = "y"
        if self.n > 500:
            print("WARNING: the size of the network is such that plotting could take a long time")
            a = input("type 'y' to continue and 'n' to undo\n")
        if a == "y":
            pos = nx.nx.spring_layout(self.graph, iterations=20)
            plt.figure(1)
            nx.draw_networkx(self.graph, node_size=[math.pow(self.graph.degree(v), 2) for v in self.graph])
            labels = {i: i + 1 for i in self.graph.nodes()}
            # plotting instructions
            plt.figure(2)
            nx.draw_networkx(self.social_one, node_size=[math.pow(self.social_one.degree(v), 2) for v in
                                                         self.social_one], node_color='b')

            plt.figure(3)
            nx.draw_networkx(self.social_two, node_size=[math.pow(self.social_two.degree(v), 2) for v in
                                                         self.social_two], node_color='g')
            plt.show()
        else:
            print("Plotting aborted")

    # generates the Real network and the two realizations
    def generate(self, n, m, l, s_one, s_two):
        self.n = n
        self.m = m
        self.l = l
        self.s_one = s_one
        self.s_two = s_two
        # initialization of the three networks
        self.graph = nx.barabasi_albert_graph(self.n, self.m)
        self.social_one = self.graph.copy()
        self.social_two = self.graph.copy()

        # with random independent probabilities we filter the real network to get the new partial ones
        for e in self.graph.edges_iter():
            keep_one = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
            keep_two = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
            if keep_one > self.s_one:
                self.social_one.remove_edge(e[0], e[1])
            if keep_two > self.s_two:
                self.social_two.remove_edge(e[0], e[1])

        # counting the total degree to assess the increased sparsity of the derived networks, selection of
        # the trusted link set
        nodes_real = self.graph.nodes()
        nodes_one = self.social_one.nodes()
        nodes_two = self.social_two.nodes()

        identified_connections = []

        for i in nodes_real:
            if i not in nodes_one or i not in nodes_two:
                print("Graph reduction error")
            d_one_i = self.social_one.degree(i)
            d_two_i = self.social_two.degree(i)
            d_graph_i = self.graph.degree(i)
            self.tot_degree_one += d_one_i
            self.tot_degree_real += d_graph_i
            self.tot_degree_two += d_two_i
            self.d_graph = max(d_graph_i, self.d_graph)
            self.d_one = max(d_one_i, self.d_one)
            self.d_two = max(d_two_i, self.d_two)
            link_known = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
            if link_known < self.l:
                identified_connections.append((i, i))

        # Printing and plotting
        print("\nDegree Background graph: ",self.tot_degree_real,"\nDegree 1st graph: ",self.tot_degree_one,"\nDegree 2nd graph", self.tot_degree_two,"\n")
        self.identified_connections = identified_connections

    def get_network(self):
        return self.graph

    def get_realizations(self):
        return self.social_one, self.social_two, self.identified_connections

    def get_maxdegree(self):
        return max(self.d_one, self.d_two)

def GetGenerator():
    return NetworkGenerator()

