import numpy as np
import sys
import pickle

task_id = int(sys.argv[1])
colors = str(sys.argv[2])
properedges  = np.load("./data/properedges_"+colors+"color.npy")
all_graphsb = np.load("./data/all_graphs.npy")

all_subgraphs = np.array([['{0:036b}'.format(int(edges,2) & int(mono,2)) for mono in properedges] for edges in all_graphsb[(task_id-1)*3000: task_id*3000]])
with open("./data/isoclass", "rb") as fp:   # Unpickling
    ISOCLASSES = pickle.load(fp)

mat = np.zeros((all_subgraphs.shape[0], len(ISOCLASSES)))

for i in range(len(all_subgraphs)):
    for j in range(len(ISOCLASSES)): # contains the edge list of all possible graphs in the isoclass
        if ISOCLASSES[j] is None:
            mat[i][j]=0
        else:
            mat[i][j] = np.count_nonzero([subgraph in ISOCLASSES[j] for subgraph in all_subgraphs[i]])

with open("./data/mat"+str((task_id-1)*3000)+str(task_id*3000)+".npy", "wb") as f:
    np.save(f, mat)
