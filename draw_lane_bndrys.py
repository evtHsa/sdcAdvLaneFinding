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

def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    init_img, binary_warped = iu.get_binary_warped_image(path, cd, pd, vwr=None)
    lane = lu.Lane(cd, pd, img = init_img, units='pixels', vwr=None)
    ut.oneShotMsg("FIXME: change pixels in prev line to meters")
    iv._push(vwr, init_img)
    iv._push(vwr, binary_warped)
    lane.find_pixels_all_bndrys(binary_warped)
    lane.fit_polynomials()
    lane_img = lane.get_image(init_img)
    iv._push(vwr, lane_img)
    size = (lane_img.shape()[1], lane_img.shape()[0])
    lane_img = iu.cv2WarpPerspective(lane_img, cd['M_lookdown_inv'], size, vwr=None)
    iv._push(vwr, lane_img)
    blended_img = iu.cv2AddWeighted(init_img, lane_img,
                                    alpha = pd['lane_blend_alpha'],
                                    beta = pd['lane_blend_beta'],
                                    gamma = pd['lane_blend_gamma'], title = "merged")
    iv._push(vwr, blended_img)
    vwr.show()

    ut.oneShotMsg("FIXME: this routine needs 2move to LaneUtils w/appropriate name")

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
cache_dict['fit_units'] = 'pixels'
vwr = cache_dict['viewer']

for path in ut.get_fnames("test_images/", "*.jpg"):
    print("FIXME: path = %s" % path)
    doit(path=path, cd=cache_dict, pd=parm_dict, vwr=vwr)
