from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt
from Derivative import *
from Path import *
import h5py
import cv2

img_path = './north-bend.jpg'
img = cv2.imread(img_path, 0) 
X0 = cv2.resize(img, (int(732/2), int(1024/2)))
shape = X0.shape
mx = shape[0]
my = shape[1]
#print('image.shape', img.shape)

X0 = np.flip(X0)

dXg, dYg = computeDerivativesCentral(X0)
dX, dY = streamVectorsCentral(X0)

d = gradientMagnitudeCentral(X0)

print('X0', X0.shape)
print('dX',dX.shape)

#Compute the location of the maximum gradients
gradList = sortAbs(X0)

#using the first element in the dictionary follow the streamvectors
pos = gradList[0]['pos']

#Try and parametrize the image starting at the given position.
path = Path(dX, dY, pos[0], pos[1])

path = np.array(path)

plt.subplot(2,2,1)
plt.pcolor(X0[1:mx-1,1:my-1])
plt.title('original image from mnist')

plt.subplot(2,2,2)
plt.pcolor(X0[1:mx-1,1:my-1])
plt.plot(path[:,0],path[:,1],color='red')
plt.title('parameterization')

plt.subplot(2,2,3)
plt.quiver(dX, dY, units='width', scale=2000)
plt.title('stream vectors')

plt.subplot(2,2,4)
plt.quiver(dXg, dYg, units='width', scale=2000)
plt.title('gradient vectors')

plt.show()