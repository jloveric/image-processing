import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3" 

import unittest
from snovalleyai_image_processing import *
import numpy as np

class TestFunctions(unittest.TestCase):

    def test_basis(self):
        # Basic test that there is no crash.
        # TODO: port the c++ tests over
        # stub for now
        pass


if __name__ == '__main__':
    unittest.main()