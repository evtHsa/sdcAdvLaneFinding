#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import LaneUtils as lu

ut.brk("this is broken since recent interface change")
def doit(path="", cd=None, pd=None, vwr=None):
    for path in ut.get_fnames("test_images/", "*.jpg"):
        lane = lu.Lane(cd, pd, vwr)
        vwr.flush()
        print("FIXME: path = %s" % path)
        init_img, binary_warped = iu.get_binary_warped_image(path, cd, pd, vwr)
        iv._push(vwr, init_img)
        iv._push(vwr, binary_warped)
        lane.find_pixels_all_bndrys(binary_warped)
        lane.fit_polynomials()
        vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cache_dict['viewer']
doit(cd=cache_dict, pd=parm_dict, vwr=vwr)

