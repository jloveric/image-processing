from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt
from snovalleyai_image_processing.Derivative import *
from snovalleyai_image_processing.Path import *

import h5py
import cv2

img_path = './north-bend.jpg'
img = cv2.imread(img_path, 0) 
#X0 = cv2.resize(img, (int(732/4), int(1024/4)))
X0 = cv2.resize(img, (500, 500))
shape = X0.shape
mx = shape[0]
my = shape[1]

print('x0', X0)



X0 = np.int16(np.flip(X0))

dXg, dYg = computeDerivativesCentral(X0)
dX, dY = streamVectorsCentral(X0)

d = gradientMagnitudeCentral(X0)

print('X0', X0.shape)
print('dX',dX.shape)

#Compute the location of the maximum gradients
gradList = sortAbs(X0)

maxPaths = 1000

pathList = []
for i in range(0,maxPaths) :
    #using the first element in the dictionary follow the streamvectors
    pos = gradList[i]['pos']

    #Try and parametrize the image starting at the given position.
    path = Path(dX, dY, pos[0], pos[1])

    path = np.array(path)
    pathList.append(path)

plt.subplot(2,2,1)
plt.pcolor(X0[1:mx-1,1:my-1])
plt.title('Original image')

plt.subplot(2,2,2)
plt.pcolor(X0[1:mx-1,1:my-1])
for i in range(0,maxPaths) :
    plt.plot(pathList[i][:,0],pathList[i][:,1],color='red')
plt.title('Parameterization')

plt.subplot(2,2,3)
plt.quiver(dX[0:dX.shape[0]:4, 0:dX.shape[1]:4], dY[0:dX.shape[0]:4, 0:dX.shape[1]:4], units='width', scale=1000)
plt.title('Stream vectors')

plt.subplot(2,2,4)
plt.pcolor(d)
#plt.plot(path[:,0],path[:,1],color='red')
plt.title('Gradient magnitude')

#plt.subplot(2,2,4)
#plt.quiver(dXg[0:dX.shape[0]:4, 0:dX.shape[1]:4], dYg[0:dX.shape[0]:4, 0:dX.shape[1]:4], units='width', scale=5000)
#plt.title('gradient vectors')

plt.show()