"""""
This file is part of "Implementation of an Efficient Reconciliation Algorithm for Social Network".

"Implementation of an Efficient Reconciliation Algorithm for Social Network"
is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"Implementation of an Efficient Reconciliation Algorithm for Social Network"
is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

If you are willing to know more about the above mentioned license
see <http://www.gnu.org/licenses/>.

For what the algorithmic part is concerned we base the implementation on
the paper http://www.vldb.org/pvldb/vol7/p377-korula.pdf (also available
in the informative_materials folder of the repo.
"""

import matplotlib.pyplot as plt
import networkx as nx
import math
import os


class NetworkGenerator(object):
    # Graph variable representing the real underlying network
    n = 0
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
    def generate(self, n, m, l, s_one, s_two, verbosity=False):
        self.n = n
        # initialization of the three networks
        self.graph = nx.barabasi_albert_graph(n, m)
        self.social_one = self.graph.copy()
        self.social_two = self.graph.copy()

        # with random independent probabilities we filter the real network to get the new partial ones
        for e in self.graph.edges_iter():
            keep_one = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
            keep_two = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
            if keep_one > s_one:
                self.social_one.remove_edge(e[0], e[1])
            if keep_two > s_two:
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
            if link_known < l:
                identified_connections.append((i, i))

        # Printing and plotting
        if verbosity:
            print("\nDegree Background graph: ", self.tot_degree_real,
                  "\nDegree 1st graph: ", self.tot_degree_one, "\nDegree 2nd graph", self.tot_degree_two, "\n")

        self.identified_connections = identified_connections

    def get_network(self):
        return self.graph

    def get_realizations(self):
        return self.social_one, self.social_two, self.identified_connections

    def get_max_degree(self):
        return max(self.d_one, self.d_two)


def get_generator():
    return NetworkGenerator()
