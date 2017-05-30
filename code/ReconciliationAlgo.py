import math as m
import networkx as nx

class Reconciliator():

    bests_one = {}
    bests_two = {}

    def reconcile_naive(self, g1, g2, L, k, D, T):
        local = []
        for i in range(0, k):
            for j in range(m.floor(m.log(D,2)), 1, -1):
                print(i, j)
                identified_one = [l[0] for l in L]
                identified_two = [l[1] for l in L]
                g1_nodes = [u for u in list(set(g1.nodes())-set(identified_one))]
                g2_nodes = [u for u in list(set(g2.nodes())-set(identified_two))]
                d_thresh = m.pow(2, j)
                for u in g1_nodes:
                    self.bests_one[u] = (0, [-1])
                    for v in g2_nodes:
                        score = 0
                        if g1.degree(u) > d_thresh and g2.degree(v) > d_thresh:
                            for i in L:
                                if i[0] in g1.neighbors(u) and i[1] in g2.neighbors(v):
                                    score += 1
                            if score > T:
                                a = self.bests_one[u]
                                if v not in self.bests_two.keys():
                                    self.bests_two[v] = (0, [-1])
                                b = self.bests_two[v]
                                if score >= a[0] and score >= b[0]:
                                    if score > a[0]:
                                        self.bests_one[u] = (score, [])
                                    if score > b[0]:
                                        self.bests_one[u] = (score, [])
                                    self.bests_one[u][1].append(v)
                                    self.bests_two[v][1].append(u)
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


def get_reconciliator():
    return Reconciliator()



