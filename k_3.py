import numpy as np
import networkx as nx


q = 2

# we have a c_H for each of the 25 2-colorable graphs on 9 vertices
# we iterate over all 274668 G_9 unlabeled graphs on 9 vertices

#checks prop 2.5 for graphs up to 9 vertices
def check_with_coeffs(coeffs):
    # check condition (2) by iterating through all 2-colorings of all graphs with up to 9 vertices

    mat = np.load('k3_subg_counts_9v2.npy')

    new_mat = np.array(mat[:19])/2**9
    # graphs contains all unlabeled graphs G_9 with up to 9 vertices ranked in increasing order of edges
    # some might not be 2 colorable

    graphs = sorted(nx.read_graph6("graph9.g6"), key = lambda G: G.number_of_edges())[:len(mat)]
    print("Checking ",  len(graphs), " constraints.")
    max_found = 0
    for i, G in enumerate(graphs):
        if i == 0:
            continue

        # we have a coefficient (c_H) for each of the 2-colorable graph on at most 9 vertices
        # sum (|c_H| * #{G_q ~ H})
        # hence mat[i][j] = the number of G_q which is a subset of G_9[i] such that G_q ~ H[j]
        s = abs(sum(mat[i][j] * coeffs[j] for j in range(len(coeffs))))
        if s > max_found:
            print("s=",s,"max_found=",max_found)
            # 2^9 * 1000, 1000 because all coeff are scaled by 1000
            if s != 512000: # if the H is not empty
                max_found = s
            print("Absolute value of ", s, "/512000 = ", round(s/512000,4), " achieved by graph ", G.edges())

        elif i %10000 == 0:
            print("Checked ", i, "/", len(graphs))
    print ("Complete")
        

#prunes isolated nodes from a list of graphs
def isoclasses(graphs):
    copies = []
    for G in graphs:
        H = G.copy()
        H.remove_nodes_from(list(nx.isolates(H)))
        copies += [H]
    return copies


#computs the bound in prop 3.5
def count_bounds_with_coeffs(coeffs):
    # condition (3) is verified for graphs with more than 9 vertices by applying proposition 3.5 to all graphs with n_0 = 9
    # iterating through all 2-colorings of all graphs with up to 9 vertices.

    constr_mat = np.load('k3_subg_counts_9v2.npy')
    graphs = sorted(nx.read_graph6("graph9.g6"), key = lambda G: G.number_of_edges())[:len(constr_mat)]

    print("Checking ",  len(graphs), " constraints.")

    max_count = 0
    # max_ind = 0
    # best_counts = []
    for i, G in enumerate(graphs):
        
        row = constr_mat[i]
        extra_comps = len(list(nx.connected_components(G))) - 1
        count = sum(abs(row[j] * coeffs[j] * DC(vertices(j))) for j in range(len(coeffs))) / int(2 ** extra_comps)
        if count > max_count:
            # max_ind = i
            max_count = count
            # best_counts = [row[j] / 2 ** extra_comps for j in range(len(coeffs))]
            # 168 since DC is scaled by 168, 1000 since coefficient is scaled by 1000, 2**9 to make it the probability over all 2-coloring
            # TODO: 324000*3^9 ?? why scaling ??
            print("Value of ", count, "/324000*3^9 = ", round(count/(168000*(2 ** 9)),4), " achieved by graph ", G.edges())
        if i % 10000 == 0:
            print("Checked ", i, "/", len(graphs))
    print ("Complete")
    

# For integer computation returns 168 * DC_{2,9}(n)
# section 3.2
def DC(n):
    dc_vals = [1/2, 0, 5/8, 5/7, 5/6, 1]
    dc_vals_int = [int(x * 168) for x in dc_vals]
    if n < len(dc_vals):
        return dc_vals_int[n]
    return 50

# Number of non-isolated vertices of each graph in the list
def vertices(ind):
    verts = [0, 2, 3, 4, 4, 5, 3, 4, 6, 5, 6, 4, 5, 6, 4, 0, 0, 0, 5]
    if ind < len(verts):
        return verts[ind]
    return 10



if __name__ == "__main__":
    
    COEFFS = [7.0, -5.0, -1.0, 1.7, 3.0, 0.0, 0.0, 0.3, 0.0, -0.2, 0.0, 0.0, 0.0, 0.0, -3.7, 0.0, 0.0, 0.0, -0.75]
    # # computed from the maximum value of |c_H'| over all graphs H' which may be transformed to H by repeatedly 
    # # identifying paris of disconnected vertices.
    # COEFFS_TILDE = [7.0, 5.0, 1.7, 1.7, 3.0, 0.0, 0.0, 0.3, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 3.7, 0.0, 0.0, 0.0, 0.75]
    # # TODO: is COEFFS_TILDE = [7.0, 5.0, 1.0, ...] ?? 
    # print(len(COEFFS))

    C_INT = [int(1000 * x) for x in COEFFS]
    # C_TILDE_INT = [int(1000 * x) for x in COEFFS_TILDE]
    # print ("Checking graphs up to 9 vertices... ")
    check_with_coeffs(C_INT)
    # print()
    # print ("Bounding graphs with more than 9 vertices... ")
    # count_bounds_with_coeffs(C_TILDE_INT)
    # print([DC(vertices(j))/168 for j in range(len(COEFFS))])

   
