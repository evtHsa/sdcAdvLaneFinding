#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import SlidingWindows as sw

def draw_lanes_on_blank_img(img, lanes):
    # fit must be saved in lane d/s
    lanes_img = np.zeros_like(img).astype(np.uint8)
    ut.brk("FIXME: want fn to take lane, img & draw lane stuff on img")
    ut.brk("FIXME: do new stuff")
    
def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    init_img, binary_warped = iu.get_binary_warped_image_v2(path, cd, pd, vwr=None)
    iv._push(vwr, init_img)
    iv._push(vwr, binary_warped)
    lanes = sw.find_lane_pixels(binary_warped, cd, pd, vwr=None)
    sw.fit_polynomial(lanes['L'], pd)
    iv._push(vwr, lanes['L'].out_img)
    sw.fit_polynomial(lanes['R'], pd)
    iv._push(vwr, lanes['R'].out_img)
    draw_lanes_on_blank_img(init_img, [lanes['L'], lanes['R']])
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cache_dict['viewer']

for path in ut.get_fnames("test_images/", "*.jpg"):
    print("FIXME: path = %s" % path)
    doit(path=path, cd=cache_dict, pd=parm_dict, vwr=vwr)
