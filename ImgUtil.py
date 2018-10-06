#
# functions in this file should be only those that operate on images and/or
# return images

import pdb
import ImgViewer as iv
import cv2
import matplotlib.image as mpimg
import numpy as np
import glob
import os
import util as ut

def img_read(path, viewer=None):
     img = mpimg.imread(path)
     iv._push(viewer, img, "img_read: " + path)
     return img

def img_rgb2gray(img, viewer=None):
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        iv._push(viewer, gray, "gray: ", 'Greys_r')
        return gray
        
def img_undistort(img, mtx, dist, viewer=None):
        undist = cv2.undistort(img, mtx, dist, None, mtx)
        iv._push(viewer, img, "undistort: ")
        return undist




    
