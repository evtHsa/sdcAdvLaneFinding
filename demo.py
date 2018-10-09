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

def lane_finding_take_1(path):
    #@Undistort the image using cv2.undistort() with mtx and dist
    #@Convert to grayscale
    #@ Find the chessboard corners
    # Draw corners
    # Define 4 source points (the outer 4 corners detected in the chessboard pattern)
    # Define 4 destination points (must be listed in the same order as src points!)
    # Use cv2.getPerspectiveTransform() to get M, the transform matrix
    # use cv2.warpPerspective() to apply M and warp your image to a top-down view

    gpd['cal_mtx'] , gpd['cal_dist'] = ut.calibrate_camera(None, gpd['chessboard_nx'],
                                                           gpd['chessboard_ny'], gpd['objpoints'],
                                                           gpd['imgpoints'])
    tmp = iu.img_read(path, vwr)
    tmp = iu.img_undistort(tmp, gpd['cal_mtx'], gpd['cal_dist'], vwr)
    undistorted = np.copy(tmp)
    tmp = iu.img_rgb2gray(tmp, vwr)
    gray = np.copy(tmp) # make a copy to ensure no accidental aliasing
 
    vwr.flush()
    abs_sobel = iu.abs_sobel_thresh(gray, 'x', gpd['sobel_min_thresh'],
                              gpd['sobel_max_thresh'], gpd['sobel_kernel_size'],
                              gpd['sobel_out_depth'], vwr)
    
    mag_sobel = iu.mag_thresh(gray, gpd['sobel_min_thresh'],
                              gpd['sobel_max_thresh'], gpd['sobel_kernel_size'],
                              gpd['sobel_out_depth'], vwr)

    dir_sobel = iu.dir_thresh(gray,
                              0.7, # FIXME: need new gpd['sobel_dir_thresh_min'] ?
                              1.3, # FIXME: need new gpd['sobel_dir_thresh_min'] ?
                              15, # FIXME: gpd['sobel_kernel_size'],
                              gpd['sobel_out_depth'], vwr)
    hls_thresh = iu.hls_thresh(undistorted,
                               0.35, # FIXME: shdb in gpd
                               1, #FIXME: shdb in gpd
                               vwr)
    vwr.show()
    # 4 combo
    combined = iu.combined_thresh([abs_sobel, dir_sobel, hls_thresh, mag_sobel ],
                                  "abs+dir+hls+mag", vwr)
    #3 combos
    combined = iu.combined_thresh([abs_sobel, dir_sobel, hls_thresh ],
                                  "abs+dir+hls", vwr)
    combined = iu.combined_thresh([abs_sobel, dir_sobel, mag_sobel ],
                                  "abs+dir+mag", vwr)
    combined = iu.combined_thresh([abs_sobel, hls_thresh, mag_sobel ],
                                  "abs+hls+mag", vwr)
    #2 combos
    combined = iu.combined_thresh([abs_sobel, dir_sobel ],
                                  "abs+dir", vwr)
    combined = iu.combined_thresh([abs_sobel,  hls_thresh ],
                                  "abs+hls", vwr)
    combined = iu.combined_thresh([abs_sobel, mag_sobel ],
                                  "abs+mag", vwr)
    vwr.show()

# adapted from lesson 6.12 color and gradient
#
# FIXME: to be useful the args shd come from gpd
#
# see interesting things note in
#
# https://classroom.udacity.com/nanodegrees/nd013/parts/edf28735-efc1-4b99-8fbb-ba9c432239c8/modules/5d1efbaa-27d0-4ad5-a67a-48729ccebd9c/lessons/144d538f-335d-454d-beb2-b1736ec204cb/concepts/a1b70df9-638b-46bb-8af0-12c43dcfd0b4
def pipeline_6_12_hls(path, s_thresh=(170, 255), sx_thresh=(20, 100), vwr=None):
     
     img = iu.img_read(path, vwr)
     
      # Convert to HLS color space and separate the V channel
     hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
     h_channel = hls[:,:,0]
     l_channel = hls[:,:,1]
     s_channel = hls[:,:,2]
     iv._push(vwr, np.squeeze(h_channel), "h_channel", cmap='gray')
     iv._push(vwr, np.squeeze(l_channel), "l_channel", cmap='gray')
     iv._push(vwr, np.squeeze(s_channel), "s_channel", cmap='gray') # shows lines well
     
     # Sobel x
     sobelx = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0) # Take the derivative in x
     abs_sobelx = np.absolute(sobelx) # Abs x drvtv to accentuate lines away from horizontal
     scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
     iv._push(vwr, np.squeeze(scaled_sobel), "scaled_sobel", cmap='gray')
     ##
     
     # Threshold x gradient
     sxbinary = np.zeros_like(scaled_sobel)
     sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1
     
     # Threshold color channel
     s_binary = np.zeros_like(s_channel)
     s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
     iv._push(vwr, np.squeeze(s_binary), "s_binary", cmap='gray')
     # Stack each channel
     color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
     iv._push(vwr, np.squeeze(color_binary), "color_binary", cmap='gray')
     return color_binary

def doit_6_12(path, vwr=None):

     result =pipeline_6_12_hls(path, vwr=vwr)
     # Plot the result
     f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
     f.tight_layout()
     
     ax1.imshow(image)
     ax1.set_title('Original Image', fontsize=40)
     
     ax2.imshow(result)
     ax2.set_title('Pipeline Result', fontsize=40)
     plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)


def pipeline_6_12_mk2(path, color_space_id, s_thresh=(170, 255),
                       sx_thresh=(20, 100), vwr=None):
     
     img = iu.img_read(path, vwr)
     
      # Convert to HLS color space and separate the V channel
     hls = cv2.cvtColor(img, color_space_id)
     ch_0 = hls[:,:,0]
     ch_1 = hls[:,:,1]
     ch_2 = hls[:,:,2]
     iv._push(vwr, np.squeeze(ch_0), "ch_0", cmap='gray')
     iv._push(vwr, np.squeeze(ch_1), "ch_1", cmap='gray')
     iv._push(vwr, np.squeeze(ch_2), "ch_2", cmap='gray') # shows lines well
     
     # Sobel x
     sobelx = cv2.Sobel(ch_1, cv2.CV_64F, 1, 0) # Take the derivative in x
     abs_sobelx = np.absolute(sobelx) # Abs x drvtv to accentuate lines away from horizontal
     scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
     iv._push(vwr, np.squeeze(scaled_sobel), "scaled_sobel", cmap='gray')
     ##
     
     # Threshold x gradient
     sxbinary = np.zeros_like(scaled_sobel)
     sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1
     
     # Threshold color channel
     s_binary = np.zeros_like(ch_2)
     s_binary[(ch_2 >= s_thresh[0]) & (ch_2 <= s_thresh[1])] = 1
     iv._push(vwr, np.squeeze(s_binary), "s_binary", cmap='gray')
     # Stack each channel
     color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
     iv._push(vwr, np.squeeze(color_binary), "color_binary", cmap='gray')
     ut.brk("look about")
     return color_binary

