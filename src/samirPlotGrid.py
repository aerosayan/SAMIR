import numpy as np
import matplotlib.pyplot as plt


def plot(_gridFile):
    print("INF:: plotting grid file : "+_gridFile)
    # load the geometry information
    geom = np.loadtxt(_gridFile,dtype=np.float64)
    # separate the data into x and y arrays
    x1 = geom[:,0]
    y1 = geom[:,1]

    print(x1.size)
    fig = plt.figure()
    plt.plot(x1,y1,"o",markerSize = 1.5)
    plt.title("mesh");plt.grid()
    plt.show()
