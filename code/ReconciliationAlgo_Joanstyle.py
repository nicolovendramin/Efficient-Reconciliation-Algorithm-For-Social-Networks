import math as m
import networkx as nx
import pandas as pd
import numpy as np


class Reconciliator():

    bests_one = {}
    bests_two = {}

    def reconcile_naive(self, g1, g2, L, k, D, T):

        L_id_to_vertex = pd.Series(data=np.arange(len(L)), index=L)

        local = []
        for i in range(0, k):
            for j in range(m.floor(m.log(D,2)), 1, -1):
                # We use that dtype in order to make the matrix fit in the memory
                score_matrix=np.zeros((len(g1.nodes),len(g2.nodes)), dtype=np.uint16)

                print(i, j)

                identified_one = [l[0] for l in L]
                identified_two = [l[1] for l in L]

                g1_nodes = [u for u in list(set(g1.nodes())-set(identified_one))]
                g2_nodes = [u for u in list(set(g2.nodes())-set(identified_two))]

                d_thresh = m.pow(2, j)

                m=compute_scores(L,g1_nodes, g2_nodes,L,m,d_thresh)

                for row in m:
                    some_function(column)
                for u in self.bests_one.keys():
                    b = self.bests_one[u]
                    flag = True
                    if len(b[1]) == 1:
                        try:
                            a = self.bests_two[v]
                        except:
                            flag = False
                        if flag and len(a[1]) == 1 and a[1][0] == b[1][0]:
                            local.append((u, v))
        return local

def compute_scores(g1, g2,L,m,d_thresh):
    for l in L.values:
        for v in g1.neighbors(l[0]):
            for u in g2.neighbors(l[1]):
                if g1.degree(u) > d_thresh and g2.degree(v) > d_thresh:
                    m[u,v]+=1
    return m


def get_reconciliator():
    return Reconciliator()



