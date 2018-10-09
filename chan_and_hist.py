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

print(" last " + str(np.sum(A,axis=0)))


#what I wanted which sums all the color channel values down to n x n
# and then takes a column sum of that is
S2= np.sum(np.sum(npA,axis=0), axis=0)
#s2 is now the result of elementwise adding all the color channels and then column sum
print ("S2 = " + str(S2))

 
