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
# Lanes:  contain LaneBoundary(s) and attributes common to both boundaries
# LaneBoundary(s): contain attributes for a particular lane bounday
# Windows: are used to calculate lane boundaries

#cd is cache_dict, pd is parm_dict
cd, pd = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cd['viewer']

def doit():
    lane = lu.Lane(cd, pd, vwr=vwr)

    for path in ut.get_fnames("test_images/", "*.jpg"):
        in_img = iu.imRead(path, reader='cv2', vwr=vwr)
        out_img= lane.lane_finder_pipe(in_img, cd, pd, vwr=vwr)
        ut.brk("check test_out")
doit()
