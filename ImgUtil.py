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


def img_sobel(img, out_depth=-1, dx_order=0, dy_order=0, ksize=3, vwr=None):
     # CV=https://docs.opencv.org/3.0-beta
     # $CV/doc/py_tutorials/py_imgproc/py_gradients/py_gradients.html
     # $CV/modules/imgproc/doc/filtering.html?highlight=sobel#cv2.Sobel
     #     ddepth = -1 => outputsame as src
     # https://stackoverflow.com/questions/19248926/difference-of-opencv-mat-types
     #
     # cv2.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]]) → dst
     #
     print("FIXME: ksize,out_depth belong in  kpd")

     assert(len(img.shape) == 2) # grayscale
     assert(dx_order != dy_order)
     assert(ksize == 1 or ksize == 3 or ksize == 5 or ksize == 7)

     tmp = cv2.Sobel(img, out_depth, dx_order, dy_order, ksize)
     iv._push(vwr, tmp, "sobel") 
     iv._view(vwr, tmp, title="sobel_", cmap='Greys_r')
     return tmp,
        
    
#from lesson 6 "Gradients and Color Spaces", ch 3 "Applying Sobel"
# Define a function that applies Sobel x or y, 
# then takes an absolute value and applies a threshold.
# Note: calling your function with orient='x', thresh_min=5, thresh_max=100
# should produce output like the example image shown above this quiz.
def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255, ksize=3, vwr=None):
     # img is expected to be gray scale (FIXME: how to enforce?)
     # Apply the following steps to img
    # 2) Take the derivative in x or y given orient = 'x' or 'y'
    if orient == 'x':
        sobel = img_sobel(img, cv2.CV_64F, 1, 0, ksize, vwr)
    else:
        sobel = img_sobel(img, cv2.CV_64F, 0, 1, ksize, vwr)
    ut.brk("is img grayscale???")
    # 3) Take the absolute value of the derivative or gradient
    abs_sobel = np.absolute(sobel)
    # 4) Scale to 8-bit (0 - 255) then convert to type = np.uint8
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # 5) Create a mask of 1's where the scaled gradient magnitude 
            # is > thresh_min and < thresh_max
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    # 6) Return this mask as your binary_output image
    return sxbinary

