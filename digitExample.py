from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt
from snovalleyai_image_processing.Derivative import *
from snovalleyai_image_processing.Path import *
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

dXg, dYg = computeDerivativesCentral(X0)
dX, dY = streamVectorsCentral(X0)

d = gradientMagnitudeCentral(X0)

pathData = PathData(d)
maxPaths = 1
pathList = pathData.constructPathList(X0, maxPaths)

plt.subplot(2,2,1)
plt.pcolor(X0[1:27,1:27])
plt.title('original image from mnist')

plt.subplot(2,2,2)
plt.plot(pathList[0][:,0],pathList[0][:,1],color='red')
plt.title('parameterization')

plt.subplot(2,2,3)
plt.quiver(dX, dY, units='width', scale=2000)
plt.title('stream vectors')

plt.subplot(2,2,4)
plt.quiver(dXg, dYg, units='width', scale=2000)
plt.title('gradient vectors')

plt.show()