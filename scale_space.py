# Looking at curves over scale space using anisotropic diffusion to construct the space.

from snovalleyai_image_processing.Diffusion import *


from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt
from snovalleyai_image_processing.Derivative import *
from snovalleyai_image_processing.Path import *
import cv2

img_path = './north-bend.jpg'
img = cv2.imread(img_path, 0)
img = np.flip(img)
img = cv2.resize(img, (500, 500))


for i in range(9) :
    plt.subplot(3, 3, i+1)
    
    plt.pcolor(img)
    X0 = img
    shape = X0.shape
    mx = shape[0]
    my = shape[1]


    dXg, dYg = compute_derivatives_central(X0)
    dX, dY = stream_vectors_central(X0)

    d = gradient_magnitude_central(X0)

    pathData = PathData(d)

    maxPaths = 100
    pathList = pathData.constructPathList(X0, maxPaths)

    for i in range(0, maxPaths):
        plt.plot(pathList[i][:, 0], pathList[i][:, 1], color='red')

    out = diffusion(img,niter=10)
    img = out

plt.show()


'''
X0 = cv2.resize(img, (500, 500))
shape = X0.shape
mx = shape[0]
my = shape[1]

X0 = np.int16(np.flip(X0))

dXg, dYg = compute_derivatives_central(X0)
dX, dY = stream_vectors_central(X0)

d = gradient_magnitude_central(X0)

pathData = PathData(d)

maxPaths = 100
pathList = pathData.constructPathList(X0, maxPaths)

plt.subplot(2, 2, 1)
plt.pcolor(X0[1:mx-1, 1:my-1])
plt.title('Original image')

plt.subplot(2, 2, 2)
plt.pcolor(X0[1:mx-1, 1:my-1])
for i in range(0, maxPaths):
    plt.plot(pathList[i][:, 0], pathList[i][:, 1], color='red')
plt.title('Parameterization')

plt.subplot(2, 2, 3)
plt.quiver(dX[0:dX.shape[0]:4, 0:dX.shape[1]:4], dY[0:dX.shape[0]
           :4, 0:dX.shape[1]:4], units='width', scale=1000)
plt.title('Stream vectors')

plt.subplot(2, 2, 4)
plt.pcolor(d)
plt.title('Gradient magnitude')

plt.show()
'''