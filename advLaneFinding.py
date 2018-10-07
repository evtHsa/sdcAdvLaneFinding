#!/usr/bin/env python3

import util as ut
import ImgSaver as imgsvr
import ImgViewer as iv
import ImgUtil as iu
import cv2
import numpy as np

# FIXME: may want to tweak some of thse parms
# gpd -> global parm dict
gpd ={ 
    'chessboard_nx' : 9,
    'chessboard_ny' : 6,
    'objpoints' : [],
    'imgpoints': [],
    'cal_mtx' : None,
    'cal_dist': None,
    'sobel_min_thresh' : 30,
    'sobel_max_thresh' : 100,
    'sobel_kernel_size' : 3,
    'sobel_out_depth' : cv2.CV_64F
}

def lane_finding_take_1(path):
    #@Undistort the image using cv2.undistort() with mtx and dist
    #@Convert to grayscale
    #@ Find the chessboard corners
    # Draw corners
    # Define 4 source points (the outer 4 corners detected in the chessboard pattern)
    # Define 4 destination points (must be listed in the same order as src points!)
    # Use cv2.getPerspectiveTransform() to get M, the transform matrix
    # use cv2.warpPerspective() to apply M and warp your image to a top-down view
    vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1")

    gpd['cal_mtx'] , gpd['cal_dist'] = ut.calibrate_camera(None, gpd['chessboard_nx'],
                                                           gpd['chessboard_ny'], gpd['objpoints'],
                                                           gpd['imgpoints'])
    tmp = iu.img_read(path, vwr)
    tmp = iu.img_undistort(tmp, gpd['cal_mtx'], gpd['cal_dist'], vwr)
    undistorted = np.copy(tmp)
    tmp = iu.img_rgb2gray(tmp, vwr)
    gray = np.copy(tmp) # make a copy to ensure no accidental aliasing

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
                               0.5, # FIXME: shdb in gpd
                               1, #FIXME: shdb in gpd
                               vwr)
    vwr.show()

def debug_hls(path):
    vwr = iv.ImgViewer(w=5, h=5, rows=3, cols=4, title="lane_finding_take1")

    gpd['cal_mtx'] , gpd['cal_dist'] = ut.calibrate_camera(None, gpd['chessboard_nx'],
                                                           gpd['chessboard_ny'], gpd['objpoints'],
                                                           gpd['imgpoints'])
    tmp = iu.img_read(path, vwr)
    tmp = iu.img_undistort(tmp, gpd['cal_mtx'], gpd['cal_dist'], vwr)
    undistorted = np.copy(tmp)
    tmp = iu.img_rgb2gray(tmp, vwr)
    gray = np.copy(tmp) # make a copy to ensure no accidental aliasing

    vwr.flush()
    for (thresh_lo, thresh_hi) in [
            #(0,0),    # all black as expected
            #(0,1),    # mostly, but not entirely, white
            #(0, .2),  # kind of inverted(the lane lines are black)
            (.1, .3), # lane lines start to turn white but fuzzier than 0, .2
            (.2, .5),
            (.2, .7),
            (.3, .8),
            (.3, .9),
            (.5, .7), # sort of what we're going for
            (.5, .8), # ??
            (.6, .8), # ??
            (.5, .9), # pretty clear and sharp lane lines
            (.5, 1),  # ??
            (.7, .9),
            (.7, 1),
            (.8,1)
    ]:
        print("FIXME: (%d, %d)" % (thresh_lo, thresh_hi))
        hls_thresh = iu.hls_thresh(undistorted,
                                   thresh_lo, # FIXME: shdb in gpd
                                   thresh_hi, #FIXME: shdb in gpd
                                   vwr)
    vwr.show(clear=True)

debug_hls('test_images/signs_vehicles_xygrad.png')
#lane_finding_take_1('test_images/signs_vehicles_xygrad.png')


