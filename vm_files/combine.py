import numpy as np
import sys

colors = sys.argv[1]
data = []
for task_id in range(1, 100):
    try:
        data.append(np.load("./data/"+colors+"colors/mat"+str((task_id-1)*3000)+str(task_id*3000)+".npy"))
    except:
        print(str((task_id-1)*3000)+str(task_id*3000)+"not found")

with open("./data/mat"+colors+"color.npy", "wb") as f:
    np.save(f, np.vstack(data))
