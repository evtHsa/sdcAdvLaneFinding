#!/usr/bin/env python3

#in its own file so we can evolve it and share it with small unit tests

import cv2

# gpd -> global parm dict
parm_dict ={
    'viewer_width': 5,
    'viewer_height': 5,
    'viewer_rows': 3,
    'viewer_cols': 3,
    'camera_resolution' : (720, 1280), # rows, cols
    'chessboard_nx' : 9,
    'chessboard_ny' : 6,
    'objpoints' : [],
    'imgpoints': [],
    'quick_calibrate': True,
    'sobel_min_thresh' : 30,
    'sobel_max_thresh' : 100,
    'sobel_kernel_size' : 3,
    'sobel_out_depth' : cv2.CV_64F,
    'hough_rho' : 3,
    'hough_theta' : 0.2,
    'hough_min_len' : 150,
    'hough_max_gap' : 24,
    'hough_min_angle_deg' : 25, # 30 - 5
    'hough_max_angle_deg' : 65, # 60 + 5]
    'hough_min_intersect' : 100
}

# add things here as psuedo documentation
cache_dict = {
    'mtx' : None, 
    'dist' : None
}
