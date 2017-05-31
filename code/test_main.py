import networkx as nx
import NetworkGenerator as ng
import ReconciliationAlgo_Joanstyle as ra


generator = ng.GetGenerator()
generator.generate(1000, 10, 0.4, 0.5, 0.4)
g1, g2, L = generator.get_realizations()
D = generator.get_maxdegree()
l = len(L)
r = ra.get_reconciliator()
L = r.reconcile_naive(g1, g2, L, 2, D, 2)

#print(len(L), l)

