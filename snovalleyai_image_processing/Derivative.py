import numpy as np
from typing import Tuple


def compute_derivatives_tvd(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    '''
    Derivative using total variation diminishing (TVD) approach.
    https://en.wikipedia.org/wiki/Total_variation_diminishing
    Second order in smooth regions and first order in non-smooth regions.
    '''
    xSize = image.shape[1]
    ySize = image.shape[0]

    # compute dx
    dxc = np.arange(1, xSize-1)
    dxl = np.arange(0, xSize-2)
    dxr = np.arange(2, xSize)

    dL = image[:, dxc]-image[:, dxl]
    dR = image[:, dxr]-image[:, dxc]
    dc = 0.5*(dL+dR)

    dI = minmod(dL, dR, dc)
    dI = dI[1:(ySize-1), :]

    # compute dy
    dyc = np.arange(1, ySize-1)
    dyl = np.arange(0, ySize-2)
    dyr = np.arange(2, ySize)

    dL = image[dyc, :]-image[dyl, :]
    dR = image[dyr, :]-image[dyc, :]
    dc = 0.5*(dL+dR)

    dJ = minmod(dL, dR, dc)
    dJ = dJ[:, 1:(xSize-1)]

    return dI, dJ


def compute_derivatives_central(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    '''
    Derivative computed by a central difference
    Second order accurate all around.
    '''
    xSize = image.shape[1]
    ySize = image.shape[0]

    # compute dx
    dxl = np.arange(0, xSize-2)
    dxr = np.arange(2, xSize)

    dc = 0.5*(image[:, dxr]-image[:, dxl])
    dI = dc[1:(ySize-1), :]

    # compute dy
    dyl = np.arange(0, ySize-2)
    dyr = np.arange(2, ySize)

    dc = 0.5*(image[dyr, :]-image[dyl, :])
    dJ = dc[:, 1:(xSize-1)]

    return dI, dJ


def compute_derivative_ls(image):
    '''
    Least squares derivative.  This one will be the best.
    '''
    print('Not implemented yet')
    pass


def minmod(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    '''
    minmod TVD limiter.  Picks the smallest of the left, right and central difference.
    '''
    xl = np.where((np.absolute(a) < np.absolute(b)) &
                  (np.absolute(a) < np.absolute(c)), a, 0)
    xr = np.where((np.absolute(b) < np.absolute(a)) &
                  (np.absolute(b) < np.absolute(c)), b, 0)
    xc = np.where((np.absolute(c) <= np.absolute(a)) &
                  (np.absolute(c) <= np.absolute(b)), c, 0)

    return xl+xr+xc


def stream_vectors(image: np.ndarray, func) -> Tuple[np.ndarray, np.ndarray]:
    dX, dY = func(image)
    return dY, -dX


def gradient_magnitude(image: np.ndarray, func) -> np.ndarray:
    dX, dY = compute_derivatives_tvd(image)
    return np.sqrt(dX*dX+dY*dY)


def stream_vectors_central(image: np.ndarray) -> np.ndarray:
    return stream_vectors(image, compute_derivatives_central)


def stream_vectors_tvd(image: np.ndarray) -> np.ndarray:
    return stream_vectors(image, compute_derivatives_tvd)


def gradient_magnitude_central(image: np.ndarray) -> np.ndarray:
    return gradient_magnitude(image, compute_derivatives_central)


def gradient_magnitude_tvd(image: np.ndarray) -> np.ndarray:
    return gradient_magnitude(image, compute_derivatives_tvd)
