import math as math
import networkx as nx
import pandas as pd
import numpy as np


class Reconciliator():

    bests_one = {}
    bests_two = {}

    def reconcile_naive(self, g1, g2, L, k, D, T):
        len_begining=len(L)
        L_beggining=L.copy()

        v_id_to_vertex = pd.Series(data=np.arange(len(g2)), index=g2)
        u_id_to_vertex = pd.Series(data=np.arange(len(g1)), index=g1)

        for i in range(0, k):
            print("<---------New Iteration------------>")
            for j in range(math.floor(math.log(D,2)), 1, -1):
                # We use that dtype in order to make the matrix fit in the memory
                score_matrix=np.zeros((len(g1.nodes()),len(g2.nodes())), dtype=np.uint16)

                #print(i, j)

                identified_one = [l[0] for l in L]
                identified_two = [l[1] for l in L]

                g1_nodes = g1#[u for u in list(set(g1.nodes())-set(identified_one))]
                g2_nodes = g2#[u for u in list(set(g2.nodes())-set(identified_two))]

                d_thresh = math.pow(2, j)

                m=compute_scores(g1_nodes, g2_nodes,L,score_matrix,d_thresh)

                largest_positions_v=m.argmax(0)
                largest_positions_u=m.argmax(1)

                for iteration in range(1,len(largest_positions_v)):
                    a=largest_positions_u[largest_positions_v[iteration]]
                    if a==iteration:
                        L.append((u_id_to_vertex[a], v_id_to_vertex[iteration]))

                print("Step :",math.floor(math.log(D,2))-j+1," / ",math.floor(math.log(D,2)),"(D) of ", i," / ",k," (k)")
        print("<---------------------------------->")
        #print(L)
        print("L length beggining: ",len_begining)
        print("L length end: ",len(set(L)))
        print("New ones: ",set(L)-set(L_beggining))

        return L

def compute_scores(g1, g2,L,score_matrix,d_thresh):
    #self.graph = nx.barabasi_albert_graph(size(g1))
    #self.graph = nx.barabasi_albert_graph(self.n, self.m)

    for l in L:
        for v in g1.neighbors(l[0]):
            for u in g2.neighbors(l[1]):
                if g1.degree(u) > d_thresh and g2.degree(v) > d_thresh:
                    score_matrix[u,v]+=1
    return score_matrix


def get_reconciliator():
    return Reconciliator()


