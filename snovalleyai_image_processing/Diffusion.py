import numpy as np
import numpy as np
from medpy.filter.smoothing import anisotropic_diffusion


def diffusion(img: np.ndarray, niter: int = 1, kappa: float = 50, gamma: float = 0.1, voxelspacing: float = None, option: int = 1):
    # For now just call medpy.  May want something different here at some point.
    img_filtered = anisotropic_diffusion(
        img=img, niter=niter, kappa=kappa, gamma=gamma, voxelspacing=voxelspacing, option=option)
    return img_filtered
