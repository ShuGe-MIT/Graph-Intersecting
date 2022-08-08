import numpy as np
import pickle
import sys

task_id = int(sys.argv[1])
colors = str(sys.argv[2])

all_subgraphs = np.load("./data/"+colors+"colors/subgraphs"+str((task_id-1)*3000)+str(task_id*3000)+".npy")
with open("./data/isoclassk3v10", "rb") as fp:   # Unpickling
    ISOCLASSES = pickle.load(fp)

mat = np.zeros((all_subgraphs.shape[0], len(ISOCLASSES)))

for i in range(len(all_subgraphs)):
    for j in range(len(ISOCLASSES)): # contains the edge list of all possible graphs in the isoclass
        print("checked {}th isoclass".format(j))
        if ISOCLASSES[j] is None:
            mat[i][j]=0
        else:
            mat[i][j] = np.count_nonzero([subgraph in ISOCLASSES[j] for subgraph in all_subgraphs[i]])

with open("./data/"+colors+"colors/mat"+str((task_id-1)*3000)+str(task_id*3000)+".npy", "wb") as f:
    np.save(f, mat)
