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


import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Load our image
# `mpimg.imread` will load .jpg as 0-255, so normalize back to 0-1
img = mpimg.imread('test_images/straight_lines1.jpg')/255
print("img.shape = " + str(img.shape))

saver = None
vwr=None
#vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)


# for some bizzare reason, the image in the lesson, which I cant download,
# results in an n x m image, not n x m x 3
def hist(img, vwr):
    # TO-DO: Grab only the bottom half of the image
    # Lane lines are likely to be mostly vertical nearest to the car
    
    bottom_half = img[img.shape[0]//2:,:]
    #iv._push(vwr, img, "orig")
    #iv._push(vwr, bottom_half, "bottom half")
    # TO-DO: Sum across image pixels vertically - make sure to set `axis`
    # i.e. the highest areas of vertical lines should be larger values
    histogram = np.sum(bottom_half, axis=0)
    print("bottom_half.shape = " + str(bottom_half.shape))
    print("histogram.shape = " + str(histogram.shape))
    #iv._push(vwr, histogram, "histogram")
    
    return histogram

# Create histogram of image binary activations
histogram = hist(img, vwr)
#vwr.show()

# Visualize the resulting histogram
plt.plot(histogram)
plt.show()
print("wtf?")
