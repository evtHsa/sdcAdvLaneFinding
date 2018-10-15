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
     str(cv2.COLOR_BGR2HLS)   : 'bgr',
     str(cv2.COLOR_BGR2HSV)   : 'bgr',
     str(cv2.COLOR_RGB2Lab)   : 'rgb',
     str(cv2.COLOR_BGR2Lab)    : 'bgr',
     str(cv2.COLOR_RGB2Luv)    : 'rgb',
     str(cv2.COLOR_BGR2Luv)    : 'bgr'
}

colorConversion2DestTypeDict = { # FIXME: this is misguided, misleading, and bad
     str(cv2.COLOR_RGB2GRAY) : 'gray',
     str(cv2.COLOR_BGR2GRAY) : 'gray',
     str(cv2.COLOR_RGB2HLS)   : 'gray',
     str(cv2.COLOR_BGR2HLS)   : 'gray',
     str(cv2.COLOR_BGR2HSV)   : 'gray',
     str(cv2.COLOR_RGB2Lab) : 'gray',
     str(cv2.COLOR_BGR2Lab) : 'gray',
     str(cv2.COLOR_RGB2Luv) : 'gray',
     str(cv2.COLOR_BGR2Luv) : 'gray'
}

colorConversion2DestColorName = {
     str(cv2.COLOR_RGB2GRAY) : 'gray',
     str(cv2.COLOR_BGR2GRAY) : 'gray',
     str(cv2.COLOR_RGB2HLS)   : 'hls',
     str(cv2.COLOR_BGR2HLS)   : 'hls',
     str(cv2.COLOR_BGR2HSV)   : 'hsv',
     str(cv2.COLOR_RGB2Lab)   : 'lab',
     str(cv2.COLOR_BGR2Lab)   : 'lab',
     str(cv2.COLOR_RGB2Luv)   : 'luv',
     str(cv2.COLOR_BGR2Luv)   : 'luv'
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
                 type=getColorConversionDestType(color))
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

def combined_thresh(btnl, title): # bin_thresh_ndarray_list
     if not btnl:
          raise Exception("seriously?")
     assert(type(btnl) is list)
     img_data = btnl[0].img_data
     for btn in btnl[1:]:
          assert(type(btn) is Image)
          img_data = np.logical_and(img_data, btn.img_data)
     ret = Image(img_data = np.squeeze(img_data), title = title, type = 'gray')
     return ret

def imRead(path, reader=None, vwr=None):
     assert(reader == 'cv2' or reader == 'mpimg')

     title = reader + ":imread(" + path + ")"
     if (reader == 'cv2'):
          img_obj = Image(img_data = cv2.imread(path), title = title, type = 'bgr')
     else:
          img_obj = Image(img_data = cv2.imread(path), title = title, type = 'rgb')
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

def getColorConversionDestType(color):
     return colorConversion2DestTypeDict[str(color)]

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

def init_obj_points(nx, ny):
    # derived from https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials \
    # /py_calib3d/py_calibration/py_calibration.html
    #
    # expanded a little from original terse version for my understanding

    ret  = np.zeros((ny*nx,3), np.float32)
    grid  = np.mgrid[0:nx, 0:ny]
    # grid shape is (2, nx, ny)
    # 0 plane has row vectors of identical components from 1 to nx
    # 1 plane has col vectors of identical components from 1 to nx
    # ex: if  nx = 2 and ny = 3
    #[[[0, 0, 0],
    #  [1, 1, 1]],
    #                            2nd row
    # [[0, 1, 2],
    #  [0, 1, 2]]])
    grid = grid.T
    # after the transpose we have ny  x nx x 2
    # almost have the nx * ny pairs we want
    grid = grid.reshape(-1, 2)
    # now we h avegrid = [[0, 0], [1, 0], [0, 1], [1, 1], [0, 2], [1, 2]]
    ret[:,:2] = grid
    # finally we end up with
    # [[0., 0, 0.], ...,
    # [1.,  0., 0.],
    # [0.,  1., 0.],
    # [1.,   1., 0.]
    # [0.,  2., 0.],
    # [1.,   2., 0.]
    return ret

def cb_corners(parm_dict, cache_dict, max_files=0, verbose=False, vwr=None):
    # derived from same source as init_obj_points()
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    nx, ny = parm_dict['chessboard_nx'],  parm_dict['chessboard_ny']
    objp  = init_obj_points(nx, ny) # object points in 3 space

    obj_points = []
    img_points = [] # point in 2 space
    
    for fname in ut.get_fnames("camera_cal/", "calibration*.jpg"):

        img_obj = imRead(fname, reader='cv2', vwr=vwr)
        if verbose:
            print("cb_corners: fname = %s(%d, %d)" % (fname,
                                                      img_obj.shape()[0], img_obj.shape()[1]))
        gray = cv2CvtColor(img_obj, cv2.COLOR_BGR2GRAY, vwr)
        
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray.img_data, (nx,ny), None)
        
        # If found, add object points, image points
        if ret == True:
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(gray.img_data,corners,(11,11),(-1,-1),criteria)
            img_points.append(corners2)
            
            # Draw and display the corners
            cv2.drawChessboardCorners(img_obj.img_data, (nx,ny), corners2, ret)
            iv._push(vwr, img_obj)
        else:
            print("findChessboardCorners(%s) failed" % fname)

    iv._show(vwr, clear=True)
    cache_dict['obj_points'] = obj_points
    cache_dict['img_points'] = img_points
