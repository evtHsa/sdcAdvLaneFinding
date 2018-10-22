#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import SlidingWindows as sw

def draw_lanes_on_blank_img(img, lanes, lane_color, vwr=None):
    assert(len(lanes) == 2) # eventually we may want more & forget here assumed 2
    assert(type(img) is iu.Image)
    
    pts = {}
    for lane_label in ['L', 'R']:
        pts[lane_label] = lanes[lane_label].prep_fill_poly_points()
    pts['combined'] = np.hstack([pts['L'], pts['R']])

    lanes_img = iu.Image(img_data = np.zeros_like(img.img_data).astype(np.uint8),
                         title = "lane image", img_type = 'rgb')
    ut.brk("xxx")
    cv2.fillPoly(lanes_img.img_data, np.int_([pts['combined']]), lane_color)

    iv._push(vwr, lanes_img)
    vwr.show()
    
    ut.brk("FIXME: do more stuff")
    return lanes_image
    
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
    lane_img = draw_lanes_on_blank_img(init_img, lanes, pd['lane_line_color'], vwr)
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cache_dict['viewer']

for path in ut.get_fnames("test_images/", "*.jpg"):
    print("FIXME: path = %s" % path)
    doit(path=path, cd=cache_dict, pd=parm_dict, vwr=vwr)
