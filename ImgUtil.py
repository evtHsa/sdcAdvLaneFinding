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

def img_read(path, vwr=None):
     img = mpimg.imread(path)
     iv._push(vwr, img, "img_read: " + path)
     return img

def img_rgb2gray(img, vwr=None):
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        iv._push(vwr, gray, "gray: ", 'Greys_r')
        return gray
        
def img_undistort(img, mtx, dist, vwr=None):
        undist = cv2.undistort(img, mtx, dist, None, mtx)
        iv._push(vwr, img, "undistort: ")
        return undist

def img_drawChessboardCorners(img, nx, ny, corners, ret, vwr=None):
     cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
     iv._push(vwr, img, "with corners", cmap='Greys_r')
     return None


    
