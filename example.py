from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt
from Derivative import *
from Path import *
import h5py

genData = False

if genData :
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True)

    h5f = h5py.File('data.h5', 'w')
    h5f.create_dataset('dataset_1', data=X[0])
    h5f.close()

h5f = h5py.File('data.h5','r')
b = h5f['dataset_1'][:]
h5f.close()

X0 = np.flip(b.reshape((28,28)))

#dXg, dYg = computeDerivatives(X0)
dX, dY = streamVectorsCentral(X0)

d = gradientMagnitudeCentral(X0)

print('X0', X0.shape)
print('dX',dX.shape)

#Compute the location of the maximum gradients
gradList = sortAbs(X0)

#using the first element in the dictionary follow the streamvectors
pos = gradList[0]['pos']
path = Path(dX, dY, pos[0], pos[1])

path = np.array(path)

print('path', path)

#plt.pcolor(dX)
plt.plot(path[:,0],path[:,1],color='red')
plt.pcolor(X0[1:27,1:27])
#plt.quiver(dXg, dYg, units='width', scale=2000)
plt.quiver(dX, dY, units='width', scale=2000)
plt.show()