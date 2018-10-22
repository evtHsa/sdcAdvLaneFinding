#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import SlidingWindows as sw

def doit(path="", cd=None, pd=None, vwr=None):
    for path in ut.get_fnames("test_images/", "*.jpg"):
        vwr.flush()
        print("FIXME: path = %s" % path)
        binary_warped = iu.get_binary_warped_image_v2(path, cd, pd, vwr)
        lanes = sw.find_lane_pixels(binary_warped, cd, pd, vwr)
        sw.fit_polynomial(lanes['L'], pd)
        iv._push(vwr, lanes['L'].out_img)
        sw.fit_polynomial(lanes['R'], pd)
        iv._push(vwr, lanes['R'].out_img)
        ut.brk("do new stuff")
        vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cache_dict['viewer']
doit(cd=cache_dict, pd=parm_dict, vwr=vwr)

