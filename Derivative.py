import numpy as np

'''
Takes in an image as a 2 (or 3) dimensional numpy vector of the form [x, y, color] and computes
wave limited (Total Variation Diminishing) derivatives.
'''
def computeDerivatives(image) :

    xSize = image.shape[1]
    ySize = image.shape[0]

    #compute dx
    dxc = np.arange(1, xSize-1)
    dxl = np.arange(0, xSize-2)
    dxr = np.arange(2, xSize)

    dL = image[:,dxc]-image[:,dxl]
    dR = image[:,dxr]-image[:,dxc]
    dc = 0.5*(dL+dR)

    dI = minmod(dL, dR, dc)
    dI = dI[1:(ySize-1),:]

    #compute dy
    dyc = np.arange(1, ySize-1)
    dyl = np.arange(0, ySize-2)
    dyr = np.arange(2, ySize)

    dL = image[dyc,:]-image[dyl,:]
    dR = image[dyr,:]-image[dyc,:]
    dc = 0.5*(dL+dR)

    dJ = minmod(dL, dR, dc)
    dJ = dJ[:,1:(xSize-1)]

    return dI, dJ

def streamVectors(image) :
    dX, dY = computeDerivatives(image)
    return dY, -dX

def gradientMagnitude(image) :
    dX, dY = computeDerivatives(image)
    return np.sqrt(dX*dX+dY*dY)

def minmod(a, b, c) :

  xl = np.where((np.absolute(a) < np.absolute(b)) & (np.absolute(a) < np.absolute(c)), a, 0)
  xr = np.where((np.absolute(b) < np.absolute(a)) & (np.absolute(b) < np.absolute(c)), b, 0)
  xc = np.where((np.absolute(c) <= np.absolute(a)) & (np.absolute(c) <= np.absolute(b)), c, 0)
  
  return xl+xr+xc