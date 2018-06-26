import numpy as np
import matplotlib.pyplot as plt

# load the geometry information
geom = np.loadtxt("grid.dat",dtype=np.float64)
# separate the data into x and y arrays
x1 = geom[:,0]
y1 = geom[:,1]

print(x1.size)

plt.plot(x1,y1,"o",markerSize = 0.5)
plt.title("mesh");plt.grid()
plt.show()
