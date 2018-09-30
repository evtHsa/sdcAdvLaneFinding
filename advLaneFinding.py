#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import util as ut


# Load our image - this should be a new frame since last time!
binary_warped = mpimg.imread('test_images/test1.jpg')
imgViewer = ut.ImgViewer(30, 30)
for i in range(1,10):
    imgViewer.push(binary_warped, "zipnick")

imgViewer.show()
