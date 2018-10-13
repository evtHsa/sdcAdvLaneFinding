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

type_2_cmap = {
     'gray': 'Greys_r',
     'rgb' :  None,
     'bgr' : None
}

color_2_src_type = {
     str(cv2.COLOR_RGB2GRAY) : 'rgb',
     str(cv2.COLOR_BGR2GRAY) : 'bgr'
}

class Image:
     def __init__(self, img_data=None, title="", type='bgr'):
          self.img_data = img_data
          self.cmap = type_2_cmap[type] # fall down if not in dict
          self.type = type
          self.title = title
          
     def show(self):
          print("title = %s, type = %s" % (self.title, self.type))
          
     def shape(self):
          return self.img_data.shape

     def plot(self, _plt):
          rgb = self.img_data
          if self.type == 'bgr':
               rgb = cv2.cvtColor(self.img_data, cv2.COLOR_BGR2RGB)
          _plt.imshow(rgb, cmap=self.cmap)
          _plt.xlabel(self.title)
          
     def legalColorConversion(self, color):
          return self.type == color_2_src_type[str(color)]
     
def cv2CvtColor(img_obj, color, vwr=None):
     assert(type(img_obj) is Image)
     assert(img_obj.legalColorConversion(color))

     ret = Image(img_data = cv2.cvtColor(img_obj.img_data, color),
                 title = "cvtColor: " + str(color),
                 type=getColorName(color))
     iv._push(vwr, ret)
     return ret

def img_rgb2gray(img, vwr=None):
     assert(type(img) is Image)
     gray = cv2CvtColor(img, cv2.COLOR_RGB2GRAY, vwr)
     return gray

def cv2Undistort(img, mtx, dist, vwr=None):
     assert(type(img) is Image)
     undist = Image(img_data= cv2.undistort(img.img_data, mtx, dist, None, mtx),
                    title="undistorted", type=img.type)
     iv._push(vwr, undist)
     return undist

def img_drawChessboardCorners(img, nx, ny, corners, ret, vwr=None):
     assert(type(img) is Image)
     cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
     iv._push_deprecated(vwr, img, "with corners", type='FIXME:gray')
     return None


def Sobel(img, out_depth=-1, dx_order=0, dy_order=0, ksize=3, vwr=None):
     # CV=https://docs.opencv.org/3.0-beta
     # $CV/doc/py_tutorials/py_imgproc/py_gradients/py_gradients.html
     # $CV/modules/imgproc/doc/filtering.html?highlight=sobel#cv2.Sobel
     #     ddepth = -1 => outputsame as src
     # https://stackoverflow.com/questions/19248926/difference-of-opencv-mat-types
     #
     # cv2.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]]) → dst
     #
     assert(type(img) is Image)

     assert(len(img.shape) == 2) # grayscale
     assert(dx_order != dy_order)
     assert(ksize > 0)
     assert(ksize % 2 != 0)

     tmp = cv2.Sobel(img, out_depth, dx_order, dy_order, ksize)
     iv._push(vwr, tmp, "sobel", type='FIXME:gray')
     ut.oneShotMsg("FIXME:enforce supported types in push")
     return tmp
        
    
#from lesson 6 "Gradients and Color Spaces", ch 3 "Applying Sobel"
# 
# Define a function that applies Sobel x or y, 
# then takes an absolute value and applies a threshold.
# Note: calling your function with orient='x', thresh_min=5, thresh_max=100
# should produce output like the example image shown above this quiz.
def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255, ksize=3,
                     out_depth=cv2.CV_64F, vwr=None):

     assert(type(img) is Image)
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
     iv._push(vwr, np.squeeze(sxbinary), "scaled sobel", type='FIXME:gray')
     return sxbinary

#from lesson 6 "Gradients and Color Spaces", ch 3 "Magnitude of the Gradient"
# 
# Define a function that applies Sobel x and y, 
# then computes the magnitude of the gradient
# and applies a threshold
def mag_thresh(img, thresh_min=0, thresh_max=255, ksize=3,
               out_depth=cv2.CV_64F, vwr=None):
     assert(type(img) is Image)
     sobel_x = img_sobel(img, out_depth, 1, 0, ksize)
     sobel_y = img_sobel(img, out_depth, 0, 1, ksize)
     sobel_abs = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
     sobel_max = np.max(sobel_abs)
     scaled_sobel = np.uint8(255 * sobel_abs / sobel_max)
     binary_output = np.zeros_like(scaled_sobel)
     binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
     iv._push_deprecated(vwr, np.squeeze(binary_output), "sobel mag thresh", type='FIXME:gray')
     return binary_output
    
#from lesson 6 "Gradients and Color Spaces", ch 3 "Direction of the Gradient"
# 
# Define a function that applies Sobel x and y, 
# then computes the direction of the gradient
# and applies a threshold.
def dir_thresh(img, thresh_min=0, thresh_max=255, ksize=3,
               out_depth=cv2.CV_64F, vwr=None):
     assert(type(img) is Image)
     ut.hash_ndarray(img, "gray") #FIXME: matches udacity lesson

     sobel_x = img_sobel(img, out_depth, 1, 0, ksize)
     sobel_y = img_sobel(img, out_depth, 0, 1, ksize)
     ut.hash_ndarray(sobel_y, "sobel_y")
     abs_sobel_x = np.absolute(sobel_x)
     abs_sobel_y = np.absolute(sobel_y)
     grad_dir = np.arctan2(abs_sobel_y, abs_sobel_x)
     binary_output = np.zeros_like(grad_dir)
     binary_output[(grad_dir >= thresh_min) & (grad_dir <= thresh_max)] = 1
     iv._push_deprecated(vwr, np.squeeze(binary_output), "sobel dir thresh", type='FIXME:gray')
     return binary_output

# from lesson 6.11 "HLS quiz"
def hls_thresh(img, thresh_lo, thresh_hi, vwr):
     assert(type(img) is Image)
     hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
     s_chan = hls[:,:,2] # s channel is 2
     # FIXME: hmmmm, looking at s_chan, the values are in [0,1], so our thresholds
     #            of 90 & 255 are a bit off which explains the 
     binary_output = np.zeros_like(s_chan)
     binary_output[(s_chan > thresh_lo) & (s_chan <= thresh_hi)] = 1
     title = "hls_thresh(%.2f, %.2f)" % (thresh_lo, thresh_hi)
     iv._push_deprecated(vwr, np.squeeze(binary_output), title, type='FIXME:gray')
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
          assert(type(btn) is Image)
          ret = np.logical_and(ret, btn)
     iv._push_deprecated(vwr, np.squeeze(ret), title, type='FIXME:gray')
     return ret

def imRead(path, reader=None, vwr=None):
     assert(reader == 'cv2' or reader == 'mpimg')

     if (reader == 'cv2'):
          img_obj = Image(img_data = cv2.imread(path),
                          title = reader + ":imread(" + path + ")",
                          type = 'bgr')
     else:
          img_obj = Image(img_data = mpimg.imread(path),
                          title = reader + ":imread(" + path + ")",
                          type = 'rgb')
     iv._push(vwr, img_obj)
     return img_obj

def lookDownXform_src():
     return np.float32([[490, 482],[810, 482], [1250, 720],[40, 720]])

def lookDownXform_dst():
     return np.float32([[0, 0], [1280, 0], [1250, 720],[40, 720]])

def getLookDownXform(cache=None):
     src = lookDownXform_src()
     dst = lookDownXform_dst()
     M = cv2.getPerspectiveTransform(src, dst)
     M_inv = cv2.getPerspectiveTransform(dst, src)
     if cache and not ut.existsKey(cache, 'M_inv'):
          cache['M_lookdown'] = M
          cache['M_lookdown_inv'] = M_inv

def cv2WarpPerspective(img, xformMatrix, size, vwr=None):
     assert(type(img) is Image)
     img.img_data = cv2.warpPerspective(img.img_data, xformMatrix, size)
     iv._push(vwr, img)
     return img
          
def calibrateCamera(parms=None, cache = None, vwr = None):
     ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(cache['obj_points'],
                                                        cache['img_points'],
                                                        parms['camera_resolution'],
                                                        None, None)
     cache['mtx'] = mtx
     cache['dist'] = dist

color2NameDict = {
     str(cv2.COLOR_RGB2GRAY) : 'gray',
     str(cv2.COLOR_BGR2GRAY) : 'gray'
}

def getColorName(color):
     return color2NameDict[str(color)]

def undistort(img_obj, cache, vwr=None):
    assert(type(img_obj) is Image)

    undist = cv2Undistort(img_obj, cache['mtx'], cache['dist'])
    return undist

def look_down(img, cache, vwr=None):
     assert(type(img) is Image)
     img_size = (img.shape()[1], img.shape()[0])
     warped = cv2WarpPerspective(img, cache['M_lookdown'], img_size)
     iv._push(vwr, warped)
     return warped

