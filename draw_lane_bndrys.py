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

def doit(in_img, cd=None, pd=None, vwr=None):
    undistorted = iu.undistort(in_img, cd, vwr=None)
    top_down = iu.look_down(undistorted, cd, vwr)
    binary_warped = iu.hls_lab_lane_detect(top_down, cache_dict = cd, parm_dict = pd)
    lane.find_pixels_all_bndrys(binary_warped)
    lane.fit_polynomials()
    lane_img = lane.get_image(in_img)
    size = (lane_img.shape()[1], lane_img.shape()[0])
    lane_img = iu.cv2WarpPerspective(lane_img, cd['M_lookdown_inv'], size, vwr=None)
    blended_img = iu.cv2AddWeighted(in_img, lane_img,
                                    alpha = pd['lane_blend_alpha'],
                                    beta = pd['lane_blend_beta'],
                                    gamma = pd['lane_blend_gamma'], title = "merged")
    return blended_img

    ut.oneShotMsg("FIXME: this routine needs 2move to LaneUtils w/appropriate name")

#cd is cache_dict, pd is parm_dict
cd, pd = ut.app_init(viewer=True, saver=True, title="whatever")
cd['fit_units'] = 'pixels'
vwr = cd['viewer']

ut.oneShotMsg("FIXME: change pixels in prev line to meters")

vwr.flush()

for path in ut.get_fnames("test_images/", "*.jpg"):
    print("FIXME: path = %s" % path)
    in_img = iu.imRead(path, reader='cv2', vwr=None)
    lane = lu.Lane(cd, pd, img = in_img, units='pixels', vwr=None)
    ut.oneShotMsg("above is stupid, img shd not be in lane ctor")
    out_img= doit(in_img, cd, pd, vwr=vwr)
    iv._push(vwr, out_img)
    
vwr.show()
