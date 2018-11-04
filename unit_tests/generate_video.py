#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import LaneUtils as lu

# our object model
# VideoControler: contains the lane and state that persists between frames
# Lanes:  contain LaneBoundary(s) and attributes common to both boundaries
# LaneBoundary(s): contain attributes for a particular lane bounday
# Windows: are used to calculate lane boundaries
for path in [
        'project_video',
        #'challenge_video',
        #'harder_challenge_video'
]:
    #warper = iu.hls_lab_lane_detect
    #warper = iu.hls_lab_luv_lane_detect
    warper = iu.lab_luv_lane_detect

    vc = lu.VideoCtrlr(path, viewer=True, saver=True,
                       binary_warper=warper) # th-th-th-th-th-at's all folks

