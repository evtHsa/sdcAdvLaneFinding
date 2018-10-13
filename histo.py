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


saver = None
vwr=None
vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)

img = iu.imRead('test_images/straight_lines1.jpg', reader='mpimg', vwr=vwr)
print("img.shape = " + str(img.shape))
gray = iu.img_rgb2gray(img, vwr)
print("gray.shape = " + str(gray.shape))


# for some bizzare reason, the image in the lesson, which I cant download,
# results in an n x m image, not n x m x 3
def hist(img, vwr):
    # TO-DO: Grab only the bottom half of the image
    # Lane lines are likely to be mostly vertical nearest to the car
    
    bottom_half = img[img.shape[0]//2:,:]
    
    # TO-DO: Sum across image pixels vertically - make sure to set `axis`
    # i.e. the highest areas of vertical lines should be larger values
    histogram = np.sum(bottom_half, axis=0)
    print("bottom_half.shape = " + str(bottom_half.shape))
    print("gray.shape = " + str(gray.shape))
    print("histogram.shape = " + str(histogram.shape))
    #iv._push_deprecated(vwr, histogram, "", type='FIXME:gray')
    return histogram

# Create histogram of image binary activations
histogram = hist(gray, vwr)
#vwr.show()

# Visualize the resulting histogram
plt.plot(histogram)
vwr.show()
plt.show()
