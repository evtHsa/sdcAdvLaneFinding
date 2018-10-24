#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import LaneUtils as lu
    
def doit(path="", cd=None, pd=None, vwr=None):
    lane = lu.Lane(cd, pd, vwr=None)
    vwr.flush()
    init_img, binary_warped = iu.get_binary_warped_image_v2(path, cd, pd, vwr=None)
    iv._push(vwr, init_img)
    iv._push(vwr, binary_warped)
    lane.find_pixels_all_bndrys(binary_warped)
    lane.fit_polynomials()
    lane_img = lane.get_image(init_img)
    init_img_dup = iu.copy_image(init_img)
    iv._push(vwr, lane_img)
    vwr.show()

    ut.brk("FIXME: reverse warp this back to original perspective in caller")
    ut.brk("FIXME: combine images in caller")
    ut.brk("FIXME: this routine needs to move to LaneUtils")

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cache_dict['viewer']

for path in ut.get_fnames("test_images/", "*.jpg"):
    print("FIXME: path = %s" % path)
    doit(path=path, cd=cache_dict, pd=parm_dict, vwr=vwr)
