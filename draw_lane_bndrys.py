#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import LaneUtils as lu

def draw_lanes_on_blank_img(img, lanes, lane_color, vwr=None):
    # object model is broken here. we want an entity that encompasses a left & right
    # lane line and a polygon bounded by them and a region of interest
    #
    # the current model blurs lane  line and lane
    # what probably should be done: ++FIXME++
    #
    # 1) rename current Lane class to LineLine
    # 2) do some of the setup done in current doit() in Lane's ctor
    # 3) do the rest in Lane::updateImage
    # 4) put what's in this fn in Lane::draw()
    assert(len(lanes) == 2) # eventually we may want more & forget here assumed 2
    assert(type(img) is iu.Image)

    pts = np.hstack((lanes['L'].fill_poly_points(True),
                     lanes['R'].fill_poly_points(False)))


    lanes_img = iu.Image(img_data = np.zeros_like(img.img_data).astype(np.uint8),
                         title = "lane image", img_type = 'rgb')
    cv2.fillPoly(lanes_img.img_data, np.int_([pts]), lane_color)
    lanes['L'].draw_lane_line(lanes_img)
    lanes['R'].draw_lane_line(lanes_img)
    iv._push(vwr, lanes_img)
    vwr.show()
    
    ut.brk("FIXME: draw lane lines on sides of poly")
    ut.brk("FIXME: reverse warp this back to original perspective in caller")
    ut.brk("FIXME: combine images in caller")
    return lanes_image
    
def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    init_img, binary_warped = iu.get_binary_warped_image_v2(path, cd, pd, vwr=None)
    iv._push(vwr, init_img)
    iv._push(vwr, binary_warped)
    lanes = lu.find_lane_pixels(binary_warped, cd, pd, vwr=None)
    lu.fit_polynomial(lanes['L'], pd)
    iv._push(vwr, lanes['L'].out_img)
    lu.fit_polynomial(lanes['R'], pd)
    iv._push(vwr, lanes['R'].out_img)
    lane_img = draw_lanes_on_blank_img(init_img, lanes, pd['lane_fill_color'], vwr)
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cache_dict['viewer']

for path in ut.get_fnames("test_images/", "*.jpg"):
    print("FIXME: path = %s" % path)
    doit(path=path, cd=cache_dict, pd=parm_dict, vwr=vwr)
