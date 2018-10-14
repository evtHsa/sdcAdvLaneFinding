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
import parm_dict as pd

type_2_cmap = {
     'gray': 'Greys_r',
     'rgb' :  None,
     'bgr' : None
}

color_2_src_type = {
     str(cv2.COLOR_RGB2GRAY) : 'rgb',
     str(cv2.COLOR_BGR2GRAY) : 'bgr',
     str(cv2.COLOR_BGR2GRAY) : 'bgr',
     str(cv2.COLOR_RGB2HLS)   : 'rgb',
     str(cv2.COLOR_BGR2HLS)   : 'bgr'
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
          #self.show()
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

     assert(img.type == 'gray') # grayscale
     assert(dx_order != dy_order)
     assert(ksize > 0)
     assert(ksize % 2 != 0)

     tmp = Image(img_data = cv2.Sobel(img.img_data, out_depth, dx_order,
                                      dy_order, ksize), title="Sobel", type='gray')
     iv._push(vwr, tmp)
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
     # 2) Take the derivative in x or y given orient = 'x' or 'y'
     if orient == 'x':
          sobel = Sobel(img, out_depth, 1, 0, ksize)
     else:
          sobel = Sobel(img, out_depth, 0, 1, ksize)
     # 3) Take the absolute value of the derivative or gradient
     abs_sobel = np.absolute(sobel.img_data)
     # 4) Scale to 8-bit (0 - 255) then convert to type = np.uint8
     scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
     # 5) Create a mask of 1's where the scaled gradient magnitude 
     # is > thresh_min and < thresh_max
     sxbinary = np.zeros_like(scaled_sobel)
     sxbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
     # 6) Return this mask as your binary_output image
     ut.oneShotMsg("FIXME: this squeeze thing may be a problem")
     
     binary_image = Image(img_data=np.squeeze(sxbinary),
                          title="scaled_sobel", type = 'gray')
     iv._push(vwr, binary_image)
     return binary_image

#from lesson 6 "Gradients and Color Spaces", ch 3 "Magnitude of the Gradient"
# 
# Define a function that applies Sobel x and y, 
# then computes the magnitude of the gradient
# and applies a threshold
def mag_thresh(img, thresh_min=0, thresh_max=255, ksize=3,
               out_depth=cv2.CV_64F, vwr=None):
     assert(type(img) is Image)
     sobel_x = Sobel(img, out_depth, 1, 0, ksize)
     sobel_y = Sobel(img, out_depth, 0, 1, ksize)
     sobel_abs = np.sqrt(sobel_x.img_data ** 2 + sobel_y.img_data ** 2)
     sobel_max = np.max(sobel_abs)
     scaled_sobel = np.uint8(255 * sobel_abs / sobel_max)
     binary_output = np.zeros_like(scaled_sobel)
     binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
     ret = Image(img_data = np.squeeze(binary_output), title="sobel_mag_thresh",
                 type='gray')
     iv._push(vwr, ret)
     return ret
    
#from lesson 6 "Gradients and Color Spaces", ch 3 "Direction of the Gradient"
# 
# Define a function that applies Sobel x and y, 
# then computes the direction of the gradient
# and applies a threshold.
def dir_thresh(img, thresh_min=0, thresh_max=255, ksize=3,
               out_depth=cv2.CV_64F, vwr=None):
     assert(type(img) is Image)

     sobel_x = Sobel(img, out_depth, 1, 0, ksize)
     sobel_y = Sobel(img, out_depth, 0, 1, ksize)
     abs_sobel_x = np.absolute(sobel_x.img_data)
     abs_sobel_y = np.absolute(sobel_y.img_data)
     grad_dir = np.arctan2(abs_sobel_y, abs_sobel_x)
     binary_output = np.zeros_like(grad_dir)
     binary_output[(grad_dir >= thresh_min) & (grad_dir <= thresh_max)] = 1
     binary_image = Image(img_data = np.squeeze(binary_output),
                          title = "sobel dir thresh", type = 'gray')
     iv._push(vwr, binary_image)
     return binary_image

# from lesson 6.11 "HLS quiz"
def hls_thresh(img, thresh_lo, thresh_hi, vwr):
     assert(type(img) is Image)
     hls = cv2CvtColor(img, cv2.COLOR_BGR2HLS, vwr)
     s_chan = hls.img_data[:,:,2] # s channel is 2
     binary_output = np.zeros_like(s_chan)
     binary_output[(s_chan > thresh_lo) & (s_chan <= thresh_hi)] = 1
     binary_image = Image(img_data = np.squeeze(binary_output),
                          title = "hls_thresh(%.2f, %.2f)" % (thresh_lo, thresh_hi),
                          type = 'gray')
     iv._push(vwr, binary_image)
     return binary_image

def combined_thresh(btnl, title, vwr): # bin_thresh_ndarray_list
     if not btnl:
          raise Exception("seriously?")
     assert(type(btnl) is list)
     img_data = btnl[0].img_data
     for btn in btnl[1:]:
          assert(type(btn) is Image)
          img_data = np.logical_and(img_data, btn.img_data)
     ret = Image(img_data = np.squeeze(img_data), title = title, type = 'gray')
     iv._push(vwr, ret)
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
     str(cv2.COLOR_BGR2GRAY) : 'gray',
     str(cv2.COLOR_RGB2HLS)   : 'gray',
     str(cv2.COLOR_BGR2HLS)   : 'gray',
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

def infrastructure_setup(viewer, saver, title):
     # setup the saver and viewer keys in cache_diict
     # returns: parm_dict, cache_dict
     cd   = pd.cache_dict
     pd_ = pd.parm_dict

     cd['viewer'] = None
     cd['saver'] = None
     if saver:
          cd['saver'] = iS.ImgSaver()
     if viewer:
          cd['viewer'] = iv.ImgViewer(w=pd_['viewer_width'], h=pd_['viewer_height'],
                                      rows=pd_['viewer_rows'], cols=pd_['viewer_cols'],
                                      title=title, svr=cd['saver'])
     return cd, pd_

def camera_setup(cache_dict=None, parm_dict=None):
     vwr = cache_dict['viewer']
     ut.cb_corners(parm_dict, cache_dict, max_files=0, verbose=False,
                   vwr=None) #(obj,img)_points in cache
     calibrateCamera(parms=parm_dict, cache = cache_dict, vwr=vwr)
     # now have mtx and dist in cache
     
     getLookDownXform(cache_dict) # cache['M_lookdown[_inv]']

def app_init(viewer=False, saver=False, title=""):
     # on return these keys will be set in cache_dict
     #        viewer, saver, mtx, dist, M_lookdown, M_lookdown_inv
     # returns: parm_dict, cache_dict
     cache_dict, parm_dict = infrastructure_setup(viewer, saver, title)
     camera_setup(cache_dict = cache_dict, parm_dict = parm_dict)
     return (cache_dict, parm_dict)
