#!/usr/bin/env python3

import util as ut
import ImgViewer as iv
import ImgUtil as iu
import cv2
import numpy as np

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']

def lane_finding_take_1(path, cd = None, pd =None):
    #@Undistort the image using cv2.undistort() with mtx and dist from cache
    #@Convert to grayscale
    #@ Find the chessboard corners
    # Draw corners
    # Define 4 source points (the outer 4 corners detected in the chessboard pattern)
    # Define 4 destination points (must be listed in the same order as src points!)
    # Use cv2.getPerspectiveTransform() to get M, the transform matrix
    # use cv2.warpPerspective() to apply M and warp your image to a top-down view

    vwr.flush()
    tmp = iu.imRead(path, reader='cv2', vwr=vwr)
    undistorted = iu.cv2Undistort(tmp, cd['mtx'], cd['dist'], vwr)
    top_down = iu.look_down(undistorted, cd, vwr)
    gray = iu.cv2CvtColor(top_down, cv2.COLOR_BGR2GRAY, vwr)

    abs_sobel = iu.abs_sobel_thresh(gray, 'x', pd['sobel_min_thresh'],
                              pd['sobel_max_thresh'], pd['sobel_kernel_size'],
                              pd['sobel_out_depth'], vwr)
    
    mag_sobel = iu.mag_thresh(gray, pd['sobel_min_thresh'],
                              pd['sobel_max_thresh'], pd['sobel_kernel_size'],
                              pd['sobel_out_depth'], vwr)


    ut.oneShotMsg("FIXME: need parms for sobel_dir_thresh_(max,min), ksizse")
    dir_sobel = iu.dir_thresh(gray,
                              0.7, # FIXME: need new gpd['sobel_dir_thresh_min'] ?
                              1.3, # FIXME: need new gpd['sobel_dir_thresh_min'] ?
                              15, # FIXME: gpd['sobel_kernel_size'],
                              pd['sobel_out_depth'], vwr)
    ut.oneShotMsg("FIXME: need parm dict entries for hls thresh")
    hls_thresh = iu.hls_thresh(undistorted,
                               80, # FIXME: shdb in gpd
                               255, #FIXME: shdb in gpd
                               vwr)
    # 4 combo

    vwr.flush()
    print("FIXME: remove this flush")
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
    print("FIXME: combined thresholds not working too well right now")

def pipeline_6_12_hls(path, s_thresh=(170, 255), sx_thresh=(20, 100),
                      cd=None, pd =None, vwr=None):
     
    ut.oneShotMsg("FIXME: need parms for s_thresh and sx_thres")
    img = iu.imRead(path, reader='cv2', vwr=vwr)
    undistorted = iu.undistort(img, cd, vwr)
    top_down = iu.look_down(undistorted, cd, vwr)
    
    # Convert to HLS color space and separate the V channel
    hls = iu.cv2CvtColor(top_down, cv2.COLOR_BGR2HLS)
    h_channel = hls.img_data[:,:,0]
    l_channel = hls.img_data[:,:,1]
    s_channel = hls.img_data[:,:,2]

    iv._push(vwr,
             iu.Image(img_data=np.squeeze(h_channel), title="h_chan", type='gray'))
    iv._push(vwr,
             iu.Image(img_data=np.squeeze(l_channel), title="l_chan", type='gray'))
    iv._push(vwr,
             iu.Image(img_data=np.squeeze(s_channel), title="s_chan", type='gray'))

    # Sobel x
    sobelx = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0) # Take the derivative in x
    abs_sobelx = np.absolute(sobelx) # Abs x drvtv to accentuate lines away from horizontal
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
    iv._push(vwr,
             iu.Image(img_data = np.squeeze(scaled_sobel), title="scaled_sobel",
                      type='gray'))
    ##
    
    # Threshold x gradient
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1
    
    # Threshold color channel
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
    iv._push(vwr,
             iu.Image(img_data = np.squeeze(s_binary), title="sobel binary", type='gray'))

    # Stack each channel
    color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
    iv._push(vwr, # it's clear that the combo of sobel_x and s channel is best so far
             iu.Image(img_data = np.squeeze(color_binary), title="color_binary"))

    return color_binary

def doit_6_12(path, cd = None, pd =None, vwr=None):

     result =pipeline_6_12_hls(path, cd=cd, pd=pd, vwr=vwr)
     vwr.show()

def pipeline_6_12_mk2(path, color_space_id=-1, ch_slct=-1,  ch_name="",
                      s_thresh=(170, 255), sx_thresh=(20, 100), cd=None, pd=None,
                      vwr=None):
    
    img = iu.imRead(path, reader='cv2', vwr=vwr)
    undistorted = iu.undistort(img, cd, vwr)
    top_down = iu.look_down(undistorted, cd, vwr)
    
    # Convert to color_space_id and isolate desired channel
    # https://en.wikipedia.org/wiki/List_of_color_spaces_and_their_uses
    acs = iu.cv2CvtColor(top_down, color_space_id) # acs -> alternate color space

    slct_channel = acs.img_data[:,:,ch_slct]

    iv._push(vwr,
             iu.Image(img_data = np.squeeze(slct_channel), title=ch_name, type='gray'))

    # Sobel x
    sobelx = cv2.Sobel(slct_channel, cv2.CV_64F, 1, 0) # Take the derivative in x
    abs_sobelx = np.absolute(sobelx) # Abs x drvtv to accentuate lines away from horizontal
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
    iv._push(vwr, iu.Image(img_data = np.squeeze(scaled_sobel),
                           title = ch_name + ":scaled_sobel", type = 'gray'))


    
    # Threshold x gradient
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1
    
    # Threshold color channel
    s_binary = np.zeros_like(slct_channel)
    s_binary[(slct_channel >= s_thresh[0]) & (slct_channel <= s_thresh[1])] = 1
    # Stack each channel
    color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
    cb_image = iv._push(vwr, iu.Image(img_data = np.squeeze(color_binary),
                                      title = ch_name + "+sobelx",
                                      type = 'gray'))
    # there is really no advantage to this that I can see over hsv v-chan alone
    return cb_image

#lane_finding_take_1('test_images/signs_vehicles_xygrad.png',
#                    cd = cache_dict, pd=parm_dict)

#doit_6_12('test_images/bridge_shadow.jpg', cd = cache_dict, pd=parm_dict, vwr=vwr)
pipeline_6_12_mk2('test_images/bridge_shadow.jpg',
                  color_space_id = cv2.COLOR_BGR2HLS, ch_slct=2, ch_name="hls:s",
                  cd = cache_dict, pd = parm_dict, vwr=vwr)

pipeline_6_12_mk2('test_images/bridge_shadow.jpg',
                  color_space_id = cv2.COLOR_BGR2HSV, ch_slct =2, ch_name="hsv:v", 
                  cd = cache_dict, pd = parm_dict,  vwr=vwr)
vwr.show()

