import numpy as np
import networkx as nx
from scipy.optimize import linprog
from math import comb

q = 2
V = 9
delta = 0.125

ALL9GRAPHS = sorted(nx.read_graph6("graph9.g6"), key = lambda G: G.number_of_edges())[:19] # 274668
ALLEDGES = np.array([g.number_of_edges() for g in ALL9GRAPHS])
ALLCC = np.array([len(list(nx.connected_components(g))) for g in ALL9GRAPHS])

ALL9BIPARTITE = ALL9GRAPHS
# ALL9BIPARTITE = []
# for g in ALL9GRAPHS:
#     if nx.is_bipartite(g): ALL9BIPARTITE.append(g)

def all_colorings(V, q=2):
    for i in range(2**V):
        b = bin(i)[2:]
        yield str(0) * (V - len(b)) + b

def prume(G, C):
    # remove monochromatic edge
    g = G.copy()
    for e in g.edges():
        if C[e[0]]==C[e[1]]: 
            g.remove_edge(e[0],e[1])
    
    # remove isolated vertex
    g.remove_nodes_from(list(nx.isolates(g)))
    return g

def count_iso_colorings(G, B):
    # B = nx.Graph(B.edges())
    return np.count_nonzero(np.array([nx.is_isomorphic(B, prume(G, C)) for C in all_colorings(V, q)]))

ISO_COUNT = np.array([[count_iso_colorings(ALL9GRAPHS[i], nx.Graph(ALL9BIPARTITE[j].edges())) for j in range(len(ALL9BIPARTITE))] for i in range(len(ALL9GRAPHS))])/2**9
print(ISO_COUNT.sum(axis = 1))

def check_condition_2(coefs):
    sums = np.apply_along_axis(lambda x: np.sum(x*coefs), 1, ISO_COUNT[:9])
    return all(np.abs(sums)[1:] <=1) and sums[0] == 7

def DC(x, q = 2, V = 9):
    return max([comb(n,V)/(q**(n-V)*comb(n-x,V-x)) for n in range(V+1,max(2*x+1,V+2))]) # TODO: upper bound is 2*x??

DCs = np.array([DC(g.number_of_edges()) for g in ALL9BIPARTITE])
print(DCs)

def check_condition_3(coefs):
    sums = np.apply_along_axis(lambda x: np.sum(x*coefs*DCs), 1, ISO_COUNT[9:]) # check graphs > 3 edges
    return np.max(sums/q**(ALLCC[9:]-1)) <= 1 - delta

def coef_tilde(coefs):
    avail = [[0],
    [1],
    [2,3],
    [3],
    [4,5,8],
    [5,8],
    [6],
    [7,5,8],
    [8],
    [9,10,13,15],
    [10,15],
    [11],
    [12,15,17],
    [13,15],
    [14,16],
    [15],
    [16],
    [17,15],
    [18,13,15,17]]
    return [max([abs(coefs[i]) for i in avail[j]]) for j in range(len(coefs))]

# all disconnected H have 0 coefficients
for x1 in np.arange(-5,0,1):
    for x2 in np.arange(-2,2,1):
        for x3 in np.arange(1.0,2.0,0.1):
            for x4 in np.arange(0,5,1):
                for x7 in np.arange(0.0,1.0,0.1):
                    for x9 in np.arange(-1.0,0.0,0.1):
                        for x12 in np.arange(-1,1,1):
                            for x14 in np.arange(-4.0,-3.0,0.1):
                                for x18 in np.arange(-1.0,-0.5,0.05):
                                    coefs = np.array([7.0,x1,x2,x3,x4,0.0,0.0,x7,0.0,x9,0.0,0.0,x12,0.0,x14,0.0,0.0,0.0,x18])
                                    res=check_condition_2(coefs)
                                    res2 = check_condition_3(coef_tilde(coefs))
                                    if res and res2:
                                        print(coefs)

# # LP_coeff attempt (incomplete)
# LP_coeff = np.repeat(ISO_COUNT, 2, axis = 0)
# LP_coeff = np.apply_along_axis(lambda x: x*np.array([1,-1]*ISO_COUNT.shape[0]), 0, LP_coeff)
# b_ub=np.ones(LP_coeff.shape[0])-LP_coeff[:,0]*7
# LP_coeff = LP_coeff[:,1:]
# res = linprog(c=np.zeros(LP_coeff.shape[1]), A_ub=LP_coeff, b_ub=np.ones(LP_coeff.shape[0]), bounds =[(7,7)]+[(None, None)]*(LP_coeff.shape[1]-1))
# print(res.x)

# coefs = np.array([7.0, -5.0, -1.0, 1.7, 3.0, 0.0, 0.0, 0.3, 0.0, -0.2, 0.0, 0.0, 0.0, 0.0, -3.7, 0.0, 0.0, 0.0, -0.75])
# # print(coef_tilde(coefs))
# res=check_condition_2(coefs)
# res2 = check_condition_3(coef_tilde(coefs))
# print(res, res2)