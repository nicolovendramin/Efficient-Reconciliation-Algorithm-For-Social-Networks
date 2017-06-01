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

import math as math
import pandas as pd
import numpy as np


class Reconciliator:

    # Those global variables will represent round by round the nodes that have already been identified
    identified_one = []
    identified_two = []

    # this function receives as parameter 2 networkx.Graph objects, a list of tuples with the shape (int,int),
    # and 3 integer values.
    # This implementation is based on the one suggested by the paper, but has been made more efficient,
    # lowering the complexity from k*log(D)*n^3  to k*log(D)*n*D^2
    def reconcile_naive(self, g1, g2, L, k, D, T, verbose=False):
        # We store the number of trusted links at the beginning and a copy of that set in order to be able
        # to evaluate the obtained performances
        len_beginning = len(L)
        l_beginning = L.copy()

        v_id_to_vertex = pd.Series(data=np.arange(len(g2)), index=g2)
        u_id_to_vertex = pd.Series(data=np.arange(len(g1)), index=g1)

        # iterate on k to repeat the procedure k times
        for i in range(0, k):
            if verbose:
                print("<---------New Iteration------------>")
            # iterating from log(D) to 2 in order to have a descending filter on the minimum degree required for
            # node matching
            for j in range(math.floor(math.log(D, 2)), 1, -1):
                # We use that dtype in order to make the matrix fit in the memory
                score_matrix = np.zeros((len(g1.nodes()), len(g2.nodes())), dtype=np.uint16)

                # We identify the list of nodes from the two graphs that have already been identified
                self.identified_one = [l[0] for l in L]
                self.identified_two = [l[1] for l in L]

                # we compute once for all the threshold for this round
                d_thresh = math.pow(2, j)

                # We call the function to compute the scores
                m = self.compute_scores(g1, g2, L, score_matrix, d_thresh)

                # With the math.argmax function we compute the position of the maximum score for each column
                # and for each row
                largest_positions_v = m.argmax(0)
                largest_positions_u = m.argmax(1)

                # We will add to the trusted links only those couples in which max_position[u] = position[v]
                # and max_position[v] = position[u]
                for iteration in range(0, len(largest_positions_v)):
                    a = largest_positions_u[largest_positions_v[iteration]]
                    # we check that the best for the row corresponding to the best for the column is the same
                    # number (basically checking a symmetry in the max for that column and row)
                    if a == iteration and score_matrix[iteration, largest_positions_v[iteration]] > T:
                        L.append((u_id_to_vertex[a], v_id_to_vertex[iteration]))

                if verbose:
                    print("Step :", math.floor(math.log(D, 2)) - j + 1, " / ", math.floor(math.log(D, 2)), "(D) of ", i,
                          " / ", k, " (k)")

        # some printing to visually check the results
        new_l = set(L)-set(l_beginning)

        if verbose:
            print("<---------------------------------->")
            print("L length beginning: ", len_beginning)
            print("L length end: ", len(set(L)))
            print("New ones: ", new_l)

        return L, new_l

    # Function for the computation of the scores
    def compute_scores(self, g1, g2, L, score_matrix, d_thresh):
        # We iterate over the set of trusted links
        for l in L:
            # for each trusted connection (a,b) we add 1 in the matrix to all the combinations c,d where
            # c belongs to the neighbourhood of a and d to the one of b
            for v in g1.neighbors(l[0]):
                # we don't need to rank the nodes of g1 that are already matched so that we filter them
                if v not in self.identified_one:
                    for u in g2.neighbors(l[1]):
                        # we don't need to rank the nodes of g2 that are already matched so that we filter them
                        if u not in self.identified_two:
                            if g1.degree(u) > d_thresh and g2.degree(v) > d_thresh:
                                score_matrix[u, v] += 1
        return score_matrix


def get_reconciliator():
    return Reconciliator()
