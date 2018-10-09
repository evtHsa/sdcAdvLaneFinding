#
# demo code, usually from the lesson excercise
# return images

import pdb
import ImgViewer as iv
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import util as ut
import ImgUtil as iu
import ImgViewer as iv

A  = [[[10, 20, 30],
        [10, 20, 30],
        [10, 20, 30]],

       [[10, 20, 30],
        [10, 20, 30],
        [10, 20, 30]],

       [[10, 20, 30],
        [10, 20, 30],
        [10, 20, 30]]]

print("A = " + str(A))

npA = np.array(A)
print("npA.shape = " + str(npA.shape))

ch0 = npA[:,:,0]
print("ch0.shape = " + str(ch0.shape))

S1 = (np.sum([ npA[:,:,i] for i in range(3)], axis = 2))
print("S1 = " + str(S1))
print ("S1 = " + str(S1))

