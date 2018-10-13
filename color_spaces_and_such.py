#!/usr/bin/env python3

import util as ut
import ImgViewer as iv
import ImgUtil as iu
import parm_dict as pd

parm_dict = pd.parm_dict
cache_dict = pd.cache_dict

#saver = iS.ImgSaver()
saver = None

vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)

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

    tmp = iu.imRead(path, reader='cv2', vwr=vwr)
    undistorted = iu.cv2Undistort(tmp, cd['mtx'], cd['dist'], vwr)
    
    ut.brk("shut er down ma, she's a suckin mud: fix gpd refs and hard coded stuff")
    tmp = iu.img_rgb2gray(tmp, vwr)
    gray = np.copy(tmp) # make a copy to ensure no accidental aliasing
 
    vwr.flush()
    abs_sobel = iu.abs_sobel_thresh(gray, 'x', gpd['sobel_min_thresh'],
                              gpd['sobel_max_thresh'], gpd['sobel_kernel_size'],
                              gpd['sobel_out_depth'], vwr)
    
    ut.brk("hurl")
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

lane_finding_take_1('test_images/signs_vehicles_xygrad.png',
                    pd=parm_dict, cd = cache_dict)
#demo.doit_6_12_hls('test_images/bridge_shadow.jpg', vwr=vwr)
#demo.pipeline_6_12_mk2('test_images/bridge_shadow.jpg',
#                      cv2.COLOR_RGB2HLS, vwr=vwr)
demo.pipeline_6_12_mk2('test_images/bridge_shadow.jpg', cv2.COLOR_RGB2HSV,
                       vwr=vwr)
ut.brk("barf")
