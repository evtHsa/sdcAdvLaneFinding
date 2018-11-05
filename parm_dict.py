#!/usr/bin/env python3

#in its own file so we can evolve it and share it with small unit tests

import cv2

# gpd -> global parm dict
parm_dict ={
    'viewer_width': 5,
    'viewer_height': 5,
    'viewer_rows': 4,
    'viewer_cols': 4,
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
    'hough_min_intersect' : 100,
    # herewith we begin new style of threshold parms which hopefully is less painful 2use
    'hls_thresh' : [
        (180, 193), #not too useful
        (195, 255), #best
        (0,255) #not  too usful
    ],
    'lab_thresh' : [
        (230, 255), #(L): not too useful
        (133, 253), #(a): dubious utility
        (145, 200)  #(b): not sure if this is picking up the right stuff
    ],
    'luv_thresh' : [
        (215, 255),   #(L): seeems to pick up yellow and white lines well
        (133, 253), #(U): picks up non blurry yellow
        (0, 255)      #(V): seems useless
    ],
    'rgb' : {
        'red' : [255, 0, 0],
        'green' : [0, 255, 0],
        'blue' : [0, 0,255],
        'yellow' : [255, 255, 0]
        },
    # from lesson 7.4
    'sliding_windows' : {'nwindows' : 9, 'margin' : 100, 'minpix' : 50},
    'lane_line_thickness' : 25,
    'lane_blend_alpha' : 1,
    'lane_blend_beta' : 0.3,
    'lane_blend_gamma' : 0,
    'xm_per_pix' : 3.7/700,
    'ym_per_pix' : 30/720,
    #'bad_frame_ixes' : [1047, 1049, 1050], #hls+lab problem frames
    'bad_frame_ixes' : [24,25],
    'debug_on_assert': True,
    'quit_on_assert': False
}

# stage 2
parm_dict['lane_line_color'] = parm_dict['rgb']['blue']
parm_dict['lane_fill_color'] = parm_dict['rgb']['yellow']
parm_dict['sliding_window_color'] = parm_dict['rgb']['green']

# add things here as psuedo documentation
cache_dict = {
    'mtx' : None, 
    'dist' : None
}
