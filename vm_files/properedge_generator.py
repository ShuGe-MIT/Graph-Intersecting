import itertools
import numpy as np
import sys

V = 9
q = int(sys.argv[1])

all_colorings = np.array(list(itertools.product(np.arange(0,q), repeat = V-1)),int)
all_colorings = np.hstack([np.zeros((all_colorings.shape[0], 1),int), all_colorings])
print(all_colorings.shape)
with open('./data/all_'+str(q)+'colorings_9.npy', 'wb') as f:
    np.save(f, all_colorings)


# convert pair of vertex indices to indices in edge list
X, Y  = np.ix_(np.arange(9),np.arange(9))
convert_idx = np.triu(X*(2*V-1-X)//2-X-1 + Y, 1)
convert_idx = convert_idx + convert_idx.T

# a function to generate the monochromatic edge list from vertexgs
idx, = np.ix_(np.arange(9))
def monoedge(colorings):
    mono = np.ones(V*(V-1)//2,dtype = bool)
    for color in range(q):
        color_ind = colorings == color
        mono[[convert_idx[i,j] for i,j in itertools.combinations(idx[color_ind], 2)]] = 0
    return "".join(mono.astype(int).astype(str))

properedges = np.apply_along_axis(monoedge,1,all_colorings)
with open("./data/properedges_"+str(q)+"color.npy", "wb") as f:
    np.save(f, properedges)
print(properedges.shape)
