import numpy as np
import sys

task_id = int(sys.argv[1])
colors = str(sys.argv[2])
properedges  = np.load("./data/properedges_"+colors+"color.npy")
all_graphsb = np.load("./data/all_graphs.npy")

all_subgraphs = np.array([['{0:036b}'.format(int(edges,2) & int(mono,2)) for mono in properedges] for edges in all_graphsb[(task_id-1)*3000: task_id*3000]])
with open("./data/"+colors+"colors/subgraphs"+str((task_id-1)*3000)+str(task_id*3000)+".npy", "wb") as f:
    np.save(f, all_subgraphs)
