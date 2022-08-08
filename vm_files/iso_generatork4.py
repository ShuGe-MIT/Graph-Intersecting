import numpy as np
import itertools
adj_list = np.zeros((9,9), int)
# a function to count the number of vertices from an edge list
def count_v(adj):
    return np.count_nonzero(np.sum(adj, axis = 1)>0)

def edge(V):
    for v in itertools.combinations(np.arange(0,V), 2):
        new = np.zeros((V,V), bool)
        new[v[0],v[1]] = True
        yield np.logical_xor(new, new.T)

def path2(V):
    for v in itertools.combinations(np.arange(0,V), 3):
        for i in v:
            new = np.zeros((V,V), bool)
            for j in v:
                if j!=i:
                    new[i][j]=True
            yield np.logical_xor(new, new.T)

# a function to generate the list of all t-cycles
def t_cycle(t, V):
    for v in itertools.combinations(np.arange(0,V), t):
        new = np.zeros((V,V), bool)
        new[([v[i] for i in range(-1,t-1)], [v[i] for i in range(t)])] = True
        yield np.logical_xor(new, new.T)

def cycle4_edge(V):
    for v in itertools.combinations(np.arange(0,V), 4):
        for i in [0,1]:
            new = np.zeros((V,V), bool)
            new[([v[i] for i in range(-1,4-1)], [v[i] for i in range(4)])] = True
            new[v[i], v[(i+2)%4]] = True
            yield np.logical_xor(new, new.T)

def cycle4_cross(V):
    for v in itertools.combinations(np.arange(0,V), 4):
        new = np.zeros((V,V), bool)
        new[([v[i] for i in range(-1,4-1)], [v[i] for i in range(4)])] = True
        new[([v[0],v[1]], [v[2],v[3]])] = True
        yield np.logical_xor(new, new.T)

def cycle4_path2_offset2(V):
    for v in itertools.combinations(np.arange(0,V), 5):
        for base in itertools.combinations(v, 2):
            new = np.zeros((V,V), bool)
            for b in base:
                for i in v:
                    if not i in base:
                        new[b,i] = True
            yield np.logical_xor(new, new.T)

def cycle4_path2_edge_offset2(V):
    for v in itertools.combinations(np.arange(0,V), 5):
        for base in itertools.combinations(v, 2):
            new = np.zeros((V,V), bool)
            new[base[0], base[1]] = True
            for b in base:
                for i in v:
                    if not i in base:
                        new[b,i] = True
            yield np.logical_xor(new, new.T)

def cyclet_edge(t, V): # t= 5, 6
    for v in itertools.combinations(np.arange(0,V), t):
        for i in range(t):
            new = np.zeros((V,V), bool)
            new[([v[i] for i in range(-1,t-1)], [v[i] for i in range(t)])] = True
            new[v[i], v[(i+2)%t]] = True
            yield np.logical_xor(new, new.T)

def cycle5_cross(V):
    for v in itertools.combinations(np.arange(0,V), 5):
        for i in range(5):
            new = np.zeros((V,V), bool)
            new[([v[i] for i in range(-1,5-1)], [v[i] for i in range(5)])] = True
            new[([v[i],v[(i+1)%5]], [v[(i+2)%5],v[(i+3)%5]])] = True
            yield np.logical_xor(new, new.T)

def cycle5_path2_offset1(V):
    for v in itertools.combinations(np.arange(0,V), 5):
        for i in range(5):
            new = np.zeros((V,V), bool)
            new[([v[i] for i in range(-1,5-1)], [v[i] for i in range(5)])] = True
            new[([v[i],v[i]], [v[(i+2)%5],v[(i+3)%5]])] = True
            yield np.logical_xor(new, new.T)

def cycle5_path2_offset2(V):
    for v in itertools.combinations(np.arange(0,V), 6):
        for base in itertools.combinations(v, 2):
            remain = set(v) - set(base)
            for pair in itertools.permutations(remain, 2):
                new = np.zeros((V,V), bool)
                new[pair[0], pair[1]] = True
                for i in [0,1]:
                    new[base[i], pair[i]] = True
                for free in remain-set(pair):
                    new[base[0], free] = True
                    new[base[1], free] = True
                yield np.logical_xor(new, new.T)


def cycle6_mid(V):
    for v in itertools.combinations(np.arange(0,V), 6):
        for i in range(3):
            new = np.zeros((V,V), bool)
            new[([v[i] for i in range(-1,6-1)], [v[i] for i in range(6)])] = True
            new[v[i], v[(i+3)%6]] = True
            yield np.logical_xor(new, new.T)


def check_identifying(g1, g2):
    # check that intersect at at most 1 vertex
    init_vertices = count_v(g1) + count_v(g2)
    res_vertices = count_v(np.logical_xor(g1, g2))
    return abs(init_vertices - res_vertices) <= 1

def combine(group1, group2):
    # a function to combine all blocks
    for g1 in group1:
        for g2 in group2:
            xor = np.logical_xor(g1, g2)
            yield xor

def combine(group1, group2):
    # a function to combine all blocks
    # group1 = list(group1)
    # group2 = list(group2)
    for g1 in group1:
        for g2 in group2:
            if np.count_nonzero(np.logical_and(g1,g2))==0:
                xor = np.logical_xor(g1, g2)
                if abs(count_v(g1) + count_v(g2) - count_v(xor)) <= 1:
                    yield xor

def convert_to_array(isoclass_gen, V):
    res = np.vstack([np.hstack([graph[i,i+1:] for i in range(graph.shape[0])]) for graph in isoclass_gen])
    return np.array([bin(int("".join(str(int(item)) for item in r), 2))[2:].zfill(V*(V-1)//2) for r in res])

# get all isoclasses
V = 9
isoclasses = [  
edge(V), 
path2(V), 
t_cycle(3, V), 
combine(list(combine(list(edge(V)), list(edge(V)))), list(edge(V))), 
combine(list(edge(V)), list(t_cycle(3, V))),
t_cycle(4, V),
combine(list(combine(list(combine(list(edge(V)), list(edge(V)))), list(edge(V)))), list(edge(V))), 
cycle4_edge(V),
combine(list(combine(list(edge(V)), list(t_cycle(3, V)))), list(edge(V))),
combine(list(edge(V)), list(t_cycle(4, V))),
t_cycle(5, V),
None,
cycle4_cross(V),
combine(list(edge(V)), list(cycle4_edge(V))),
combine(list(t_cycle(3, V)), list(t_cycle(3, V))),
cyclet_edge(5, V),
cycle4_path2_offset2(V),
combine(list(combine(list(combine(list(t_cycle(3,V)), list(edge(V)))), list(edge(V)))), list(edge(V))), 
combine(list(combine(list(edge(V)), list(t_cycle(4, V)))), list(edge(V))),
combine(list(edge(V)), list(t_cycle(5, V))),
t_cycle(6, V),
None,
combine(list(edge(V)), list(cycle4_cross(V))),
cycle4_path2_edge_offset2(V),
cycle5_path2_offset1(V),
cycle5_cross(V),
combine(list(combine(list(edge(V)), list(cycle4_edge(V)))), list(edge(V))),
None,
combine(list(combine(list(edge(V)), list(t_cycle(3, V)))), list(t_cycle(3, V))),
combine(list(edge(V)), list(cyclet_edge(5, V))),
combine(list(edge(V)), list(cycle4_path2_edge_offset2(V))),
combine(list(t_cycle(5, V)), list(t_cycle(4, V))),
cyclet_edge(6, V),
cycle6_mid(V),
cycle5_path2_offset2(V),
None, 
None,
None,
None
]

res = [np.array(['0'*(V*(V-1)//2)])]
for isoclass in isoclasses:
    if isoclass is None:
        res.append([])
    else:
        res.append(convert_to_array(isoclass,V))

import pickle
with open("./data/isoclass", "wb") as fp:   #Pickling
  pickle.dump(list(map(set, res)), fp)