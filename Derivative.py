import numpy as np

'''
Takes in an image as a 2 (or 3) dimensional numpy vector of the form [x, y, color] and computes
wave limited (Total Variation Diminishing) derivatives.
'''
def computeDerivatives(image) :
  
    print('inside image', image.shape)

    xSize = image.shape[0]
    ySize = image.shape[1]

    #compute dx
    dxc = np.arange(1, xSize-1)
    dxl = np.arange(0, xSize-2)
    dxr = np.arange(2, xSize)
    y = np.arange(1, ySize-1)

    dL = image[dxl,:]-image[dxc,:]
    dR = image[dxc,:]-image[dxr,:]
    dc = 0.5*(dL+dR)
    dI = minmod(dL, dR, dc)
    dI = dI[:,1:(ySize-1)]

    #compute dy
    dyc = np.arange(1, ySize-1)
    dyt = np.arange(0, ySize-2)
    dyb = np.arange(2, ySize)
    x = np.arange(1, xSize-1)

    dL = image[:,dyt]-image[:,dyc]
    dR = image[:,dyc]-image[:,dyb]
    dc = 0.5*(dL+dR)

    dJ = minmod(dL, dR, dc)
    dJ = dJ[1:(xSize-1),:]

    return dI, dJ

def streamVectors(image) :
    dX, dY = computeDerivatives(image)
    return dY, -dX

def minmod(a, b, c) :

  shape = a.shape
  a=a.flatten()
  b=b.flatten()
  c=c.flatten()

  xl = np.where((np.absolute(a) < np.absolute(b)) & (np.absolute(a) < np.absolute(c)), a, 0)
  xr = np.where((np.absolute(b) < np.absolute(a)) & (np.absolute(b) < np.absolute(c)), b, 0)
  xc = np.where((np.absolute(c) <= np.absolute(a)) & (np.absolute(c) <= np.absolute(b)), c, 0)
  
  xl=xl.reshape(shape)
  xr=xr.reshape(shape)
  xc=xc.reshape(shape)

  return xl+xr+xc