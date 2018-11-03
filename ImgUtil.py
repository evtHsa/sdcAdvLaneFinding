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
import copy

type_2_cmap = {
     'gray': 'Greys_r',
     'rgb' :  None,
     'bgr' : None
}

color_2_src_type = {
     str(cv2.COLOR_RGB2BGR) : 'rgb',
     str(cv2.COLOR_BGR2RGB) : 'bgr',
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
     str(cv2.COLOR_BGR2RGB) : 'rgb',
     str(cv2.COLOR_RGB2BGR) : 'bgr',
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
     str(cv2.COLOR_RGB2BGR) : 'bgr',
     str(cv2.COLOR_BGR2RGB) : 'rgb',
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
     def __init__(self, img_data=None, title="", img_type='bgr'):
          self.img_data = img_data
          self.cmap = type_2_cmap[img_type] # fall down if not in dict
          self.img_type = img_type
          self.title = title
          self.msgs = []

     def shape(self):
          return self.img_data.shape
     
     def show(self):
          print("title = %s, img_type = %s" % (self.title, self.img_type))
          
     def is2D(self):
          return len(self.img_data.shape) == 2
          
     def shape(self):
          return self.img_data.shape

     def putText(self):
          # https://stackoverflow.com/questions/37191008/load-truetype-font-to-opencv
          # questions/16615662/how-to-write-text-on-a-image-in-windows-using-python-opencv2
          r, g, b = (255, 255, 255) # FIXME: what if img is rbg, enforcement??
          font=cv2.FONT_HERSHEY_DUPLEX #why are hershey the only fonts in opencv
          y = 50
          for msg in self.msgs:
               cv2.putText(self.img_data, msg, (50, y), font, 2, (r, g, b), 2, cv2.LINE_AA)
               y += 50 # I hate guessing about magic #s! ho w tall is the text??
                    
     def plot(self, _plt):
          #self.show()
          rgb = self.img_data
          if self.img_type == 'bgr':
               rgb = cv2.cvtColor(self.img_data, cv2.COLOR_BGR2RGB)
          if len(rgb.shape) == 1:
               _plt.plot(rgb) # histogram or other 1D thing
          else:
               _plt.imshow(rgb, cmap=self.cmap)
          _plt.xlabel(self.title)
          
     def legalColorConversion(self, color):
          # FIXME: just say yes until we have better fix for the fact that
          # cv2.COLOR_RGB2BGR == cv2.COLOR_BGR2RGB
          #return self.img_type == color_2_src_type[str(color)]
          return True
     
def cv2CvtColor(img_obj, color, vwr=None):
     assert(type(img_obj) is Image)
     ut._assert(img_obj.legalColorConversion(color))

     ret = Image(img_data = cv2.cvtColor(img_obj.img_data, color),
                 title = "cvtColor: " + str(color),
                 img_type=getColorConversionDestType(color))
     return ret

def img_rgb2gray(img, vwr=None):
     assert(type(img) is Image)
     gray = cv2CvtColor(img, cv2.COLOR_RGB2GRAY, vwr)
     return gray

def cv2Undistort(img, mtx, dist, vwr=None):
     assert(type(img) is Image)
     undist = Image(img_data= cv2.undistort(img.img_data, mtx, dist, None, mtx),
                    title="undistorted", img_type=img.img_type)
     return undist

def img_drawChessboardCorners(img, nx, ny, corners, ret, vwr=None):
     assert(type(img) is Image)
     cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
     iv._push_deprecated(vwr, img, "with corners", img_type='FIXME:gray')
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

     assert(img.img_type == 'gray') # grayscale
     assert(dx_order != dy_order)
     assert(ksize > 0)
     assert(ksize % 2 != 0)

     tmp = Image(img_data = cv2.Sobel(img.img_data, out_depth, dx_order,
                                      dy_order, ksize), title="Sobel", img_type='gray')
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
                          title="scaled_sobel", img_type = 'gray')
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
                 img_type='gray')
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
                          title = "sobel dir thresh", img_type = 'gray')
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
                          img_type = 'gray')
     return binary_image

def combined_thresh(btnl, title): # bin_thresh_ndarray_list
     if not btnl:
          raise Exception("seriously?")
     assert(type(btnl) is list)
     img_data = btnl[0].img_data
     for btn in btnl[1:]:
          assert(type(btn) is Image)
          img_data = np.logical_and(img_data, btn.img_data)
     ret = Image(img_data = np.squeeze(img_data), title = title, img_type = 'gray')
     return ret

def imRead(path, flags = None, reader=None, vwr=None):
     # note: see cv dox for imread and remember cv2.IMREAD_GRAYSCALE
     assert(reader == 'cv2' or reader == 'mpimg')

     if flags is None:
          flags = cv2.IMREAD_COLOR
     title = reader + ":imread"
     if (reader == 'cv2'):          
          if flags == cv2.IMREAD_GRAYSCALE:
               _type = 'gray'
          else:
               _type = 'bgr'
          img_obj = Image(img_data = cv2.imread(path, flags), title = title, img_type = _type)
     else:
          img_obj = Image(img_data = mpimg.imread(path), title = title, img_type = 'rgb')
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
     ret = copy_image(img)
     ret.title = 'warped'
     ret.img_data = cv2.warpPerspective(img.img_data, xformMatrix, size)
     return ret

def getColorConversionDestType(color):
     return colorConversion2DestTypeDict[str(color)]

def undistort(img_obj, cache, vwr=None):
     #FIXME: this fn and cv2Undistort seem redundant. combine them
    assert(type(img_obj) is Image)

    undist = cv2Undistort(img_obj, cache['mtx'], cache['dist'])
    return undist

def look_down(img, cache, vwr=None):
     assert(type(img) is Image)
     img_size = (img.shape()[1], img.shape()[0])
     warped = cv2WarpPerspective(img, cache['M_lookdown'], img_size)
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
    
    vwr.flush()
    for fname in ut.get_fnames("camera_cal/", "calibration*.jpg"):
        img_obj = imRead(fname, reader='cv2', vwr=vwr)
        vwr.push(img_obj)
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
            img_obj.title = img_obj.title + "_corners_drawn"
            vwr.push(img_obj)
        else:
            print("findChessboardCorners(%s) failed" % fname)

    vwr.show(clear=True)
    cache_dict['obj_points'] = obj_points
    cache_dict['img_points'] = img_points

def oneChannelInAlternateColorspace2BinaryinaryImage(img, color_space_id=-1,
                                                     ch_slct=-1, cd =None, pd=None):
     assert(type(img) is Image)
     # note: proper functionalityr requires but we dont yet enforce that image be
     #          undistorted and transformed to top down view
     cs_short_name = colorConversion2DestColorName[str(color_space_id)]
     thresh_key = cs_short_name + "_thresh"
     thresh = pd[thresh_key][ch_slct]

     # Convert to color_space_id and isolate desired channel
     # https://en.wikipedia.org/wiki/List_of_color_spaces_and_their_uses
     acs = cv2CvtColor(img, color_space_id) # acs -> alternate color space
     slct_channel = acs.img_data[:,:,ch_slct]
     title_sfx = cs_short_name + "_" +str(ch_slct)
     
     # Threshold color channel
     s_binary = np.zeros_like(slct_channel)
     s_binary[(slct_channel >= thresh[0]) & (slct_channel <= thresh[1])] = 1
     tb_image = Image(img_data = np.squeeze(s_binary),
                         title="thresh::" + title_sfx, img_type='gray')
     return tb_image

def hls_lab_lane_detect(img, cache_dict = None, parm_dict = None):
     assert(type(img) is Image)
     hls_binary_l = oneChannelInAlternateColorspace2BinaryinaryImage(img,
                                                                     cv2.COLOR_BGR2HLS, 1, cd = cache_dict,
                                                                     pd = parm_dict)
     lab_binary_b = oneChannelInAlternateColorspace2BinaryinaryImage(img,
                                                                     cv2.COLOR_BGR2Lab, 2, cd = cache_dict,
                                                                     pd = parm_dict)
     combined = np.zeros_like(hls_binary_l.img_data)
     combined[(hls_binary_l.img_data == 1) | (lab_binary_b.img_data == 1)] =1
     ret = Image(img_data = combined, title = "hls+lab", img_type='gray')
     return ret

def hls_lab_pipeline(path="", cd=None, pd=None, vwr=None):
    img = imRead(path, reader='cv2', vwr=None)
    undistorted = undistort(img, cd, vwr=None)
    top_down = look_down(undistorted, cd, vwr)
    ret = hls_lab_lane_detect(top_down, cache_dict = cd, parm_dict = pd)
    return ret

def histo_pipe(path="", cd=None, pd=None, vwr=None):
    hls_lab = hls_lab_pipeline(path, cd, pd, vwr)
    ret = hist(hls_lab, vwr)
    hist.title = "hist: " + path
    return ret

def hist(img, vwr):
    assert(type(img) is Image)
    assert(img.is2D())
    bottom_half = img.img_data[img.img_data.shape[0]//2:,:]
    # Sum across image pixels vertically - make sure to set `axis`
    # i.e. the highest areas of vertical lines should be larger values
    histogram = np.sum(bottom_half, axis=0)
    histogram = Image(img_data = histogram, title="histogram", img_type='gray')
    return histogram

def get_LR_hist_max_ix(hist):
    # see lesson 7.4
    width = hist.img_data.shape[0]
    midway = width // 2
    
    left_max_ix    = np.argmax(hist.img_data[0:midway])
    right_max_ix = midway + np.argmax(hist.img_data[midway:width])
    return (left_max_ix, right_max_ix)


def cv2Polylines(x_pts, y_pts, out_img, line_color=None, line_thickness=None):
    assert(type(out_img) is Image)
    pts = np.array(list(zip(x_pts, y_pts)), dtype=np.int32)
    cv2.polylines(out_img.img_data, [pts], False, line_color, line_thickness)

def copy_image(in_img):
     assert(type(in_img) is Image)
     return copy.deepcopy(in_img)

def cv2AddWeighted(src1, src2, alpha=None, beta=None, gamma=None, title=None):
     assert(type(src1) is Image)
     assert(type(src2) is Image)
     assert(src1.shape() == src2.shape())
     assert(not  alpha is None)
     assert(not  beta is None)
     assert(not  gamma is None)
     out_img = Image(img_data = cv2.addWeighted(src1.img_data, alpha,
                                                src2.img_data, beta, gamma),
                     title=title,
                     img_type = src1.img_type)
     return out_img
