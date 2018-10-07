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

     assert(len(img.shape) == 2) # grayscale
     assert(dx_order != dy_order)
     assert(ksize > 0)
     assert(ksize % 2 != 0)

     tmp = cv2.Sobel(img, out_depth, dx_order, dy_order, ksize)
     iv._push(vwr, tmp, "sobel", cmap='Greys_r') 
     return tmp
        
    
#from lesson 6 "Gradients and Color Spaces", ch 3 "Applying Sobel"
# 
# Define a function that applies Sobel x or y, 
# then takes an absolute value and applies a threshold.
# Note: calling your function with orient='x', thresh_min=5, thresh_max=100
# should produce output like the example image shown above this quiz.
def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255, ksize=3,
                     out_depth=cv2.CV_64F, vwr=None):
     # Apply the following steps to img
     # 2) Take the derivative in x or y given orient = 'x' or 'y'
     if orient == 'x':
          sobel = img_sobel(img, out_depth, 1, 0, ksize)
     else:
          sobel = img_sobel(img, out_depth, 0, 1, ksize)
     # 3) Take the absolute value of the derivative or gradient
     abs_sobel = np.absolute(sobel)
     # 4) Scale to 8-bit (0 - 255) then convert to type = np.uint8
     scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
     # 5) Create a mask of 1's where the scaled gradient magnitude 
     # is > thresh_min and < thresh_max
     sxbinary = np.zeros_like(scaled_sobel)
     sxbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
     # 6) Return this mask as your binary_output image
     #FIXME: this squeeze thing may be a problem
     iv._push(vwr, np.squeeze(sxbinary), "scaled sobel", cmap='Greys_r') 
     return sxbinary

#from lesson 6 "Gradients and Color Spaces", ch 3 "Magnitude of the Gradient"
# 
# Define a function that applies Sobel x and y, 
# then computes the magnitude of the gradient
# and applies a threshold
def mag_thresh(img, thresh_min=0, thresh_max=255, ksize=3,
               out_depth=cv2.CV_64F, vwr=None):
     sobel_x = img_sobel(img, out_depth, 1, 0, ksize)
     sobel_y = img_sobel(img, out_depth, 0, 1, ksize)
     sobel_abs = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
     sobel_max = np.max(sobel_abs)
     scaled_sobel = np.uint8(255 * sobel_abs / sobel_max)
     binary_output = np.zeros_like(scaled_sobel)
     binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
     iv._push(vwr, np.squeeze(binary_output), "sobel mag thresh", cmap='Greys_r') 
     return binary_output
    
#from lesson 6 "Gradients and Color Spaces", ch 3 "Direction of the Gradient"
# 
# Define a function that applies Sobel x and y, 
# then computes the direction of the gradient
# and applies a threshold.
def dir_thresh(img, thresh_min=0, thresh_max=255, ksize=3,
               out_depth=cv2.CV_64F, vwr=None):
     ut.hash_ndarray(img, "gray") #FIXME: matches udacity lesson

     sobel_x = img_sobel(img, out_depth, 1, 0, ksize)
     sobel_y = img_sobel(img, out_depth, 0, 1, ksize)
     ut.hash_ndarray(sobel_y, "sobel_y")
     abs_sobel_x = np.absolute(sobel_x)
     abs_sobel_y = np.absolute(sobel_y)
     grad_dir = np.arctan2(abs_sobel_y, abs_sobel_x)
     binary_output = np.zeros_like(grad_dir)
     binary_output[(grad_dir >= thresh_min) & (grad_dir <= thresh_max)] = 1
     iv._push(vwr, np.squeeze(binary_output), "sobel dir thresh", cmap='Greys_r') 
     return binary_output

# from lesson 6.11 "HLS quiz"
def hls_thresh(img, thresh_lo, thresh_hi, vwr):
     hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
     s_chan = hls[:,:,2] # s channel is 2
     # FIXME: hmmmm, looking at s_chan, the values are in [0,1], so our thresholds
     #            of 90 & 255 are a bit off which explains the 
     binary_output = np.zeros_like(s_chan)
     binary_output[(s_chan > thresh_lo) & (s_chan <= thresh_hi)] = 1
     title = "hls_thresh(%.2f, %.2f)" % (thresh_lo, thresh_hi)
     iv._push(vwr, np.squeeze(binary_output), title, cmap='gray')
     return binary_output

# for this to be industrial strength:
#         FIXME: ensure that the type of the arg is list
#         FIXME: ensure that every element of the list is an ndarry
#         FIXME: ensure that every array has the same shap
#         FIXME: ensure that every value in every array is either 0 or 1

def combined_thresh(btnl, title, vwr): # bin_thresh_ndarray_list
     if not btnl:
          raise Exception("seriously?")
     ret = btnl[0]
     for btn in btnl[1:]:
          ret = np.logical_and(ret, btn)
     iv._push(vwr, np.squeeze(ret), title, cmap='gray')
     return ret
