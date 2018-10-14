#!/usr/bin/env python3

import util as ut
import ImgViewer as iv
import ImgUtil as iu
import parm_dict as pd
import cv2

parm_dict = pd.parm_dict
cache_dict = pd.cache_dict

#saver = iS.ImgSaver()
saver = None

vwr = iv.ImgViewer(w=5, h=5, rows=3, cols=3, title="lane_finding_take1", svr=saver)

ut.cb_corners(parm_dict, cache_dict, max_files=0, verbose=False,
              vwr=None) #(obj,img)_points in cache
iu.calibrateCamera(parms=parm_dict, cache = cache_dict, vwr=vwr)
# now have mtx and dist in cache

iu.getLookDownXform(cache_dict) # cache['M_lookdown[_inv]']

def lane_finding_take_1(path, pd =None, cd = None):
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
                      pd =None, cd = None, vwr=None):
     
    ut.oneShotMsg("FIXEM: need parms for s_thresh and sx_thres")
    ut.brk("stuff needs porting to new scheme wicked bad")
    img = iu.imRead(path, reader='cv2', vwr=vwr)
    undistorted = iu.cv2Undistort(img, cd['mtx'], cd['dist'], vwr)
    top_down = iu.look_down(undistorted, cd, vwr)
    
    # Convert to HLS color space and separate the V channel
    hls = iu.cv2CvtColor(top_down, cv2.COLOR_RGB2HLS)
    h_channel = hls.img_data[:,:,0]
    l_channel = hls.img_data[:,:,1]
    s_channel = hls.img_data[:,:,2]
    ut.brk("debug this line by line")
    iv._push_deprecated(vwr, np.squeeze(h_channel), "h_channel", cmap='gray')
    iv._push_deprecated(vwr, np.squeeze(l_channel), "l_channel", cmap='gray')
    iv._push_deprecated(vwr, np.squeeze(s_channel), "s_channel", cmap='gray') # shows lines well
    
    # Sobel x
    sobelx = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0) # Take the derivative in x
    abs_sobelx = np.absolute(sobelx) # Abs x drvtv to accentuate lines away from horizontal
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
    iv._push_deprecated(vwr, np.squeeze(scaled_sobel), "scaled_sobel", cmap='gray')
    ##
    
    # Threshold x gradient
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1
    
    # Threshold color channel
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
    iv._push_deprecated(vwr, np.squeeze(s_binary), "s_binary", cmap='gray')
    # Stack each channel
    color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
    iv._push_deprecated(vwr, np.squeeze(color_binary), "color_binary", cmap='gray')
    return color_binary

def doit_6_12(path, pd =None, cd = None, vwr=None):

     result =pipeline_6_12_hls(path, vwr=vwr)
     ut.brk("get rid of this plot crap")
     # Plot the result
     f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
     f.tight_layout()
     
     ax1.imshow(image)
     ax1.set_title('Original Image', fontsize=40)
     
     ax2.imshow(result)
     ax2.set_title('Pipeline Result', fontsize=40)
     plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)

#lane_finding_take_1('test_images/signs_vehicles_xygrad.png',
#                    pd=parm_dict, cd = cache_dict)

doit_6_12('test_images/bridge_shadow.jpg', pd=parm_dict, cd = cache_dict, vwr=vwr)
#demo.pipeline_6_12_mk2('test_images/bridge_shadow.jpg',
#                      cv2.COLOR_RGB2HLS, vwr=vwr)
demo.pipeline_6_12_mk2('test_images/bridge_shadow.jpg', cv2.COLOR_RGB2HSV,
                       vwr=vwr)

