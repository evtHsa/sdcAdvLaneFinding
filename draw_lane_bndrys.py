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
    lane = lu.Lane(cd, pd, vwr)
    vwr.flush()
    init_img, binary_warped = iu.get_binary_warped_image_v2(path, cd, pd, vwr=None)
    iv._push(vwr, init_img)
    iv._push(vwr, binary_warped)
    lane.find_pixels_all_bndrys(binary_warped)
    lane.fit_polynomials()
    lane_img = lane.get_image(init_img)
    ut.brk("push lane img above")
    vwr.show()
    ut.brk("FIXME: probably need to flow cd, pd, vwr down from Lane")
    ut.brk("FIXME: read LaneUtils line by line for stuff 2 clean up")
    ut.brk("FIXME: reverse warp this back to original perspective in caller")
    ut.brk("FIXME: combine images in caller")
    ut.brk("FIXME: this routine needs to move to LaneUtils")
    ut.brk("FIXME: turn off vwr where excess img push in LaneUtils and push img above")

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cache_dict['viewer']

for path in ut.get_fnames("test_images/", "*.jpg"):
    print("FIXME: path = %s" % path)
    doit(path=path, cd=cache_dict, pd=parm_dict, vwr=vwr)
