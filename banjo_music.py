#!/usr/bin/env python3

import util as ut

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']

# heavily adapted from assignment 1
def hough_lines(image, parm_dict):
     ut.oneShotMsg("FIXME: this needs to be in ImgUtil")
     assert(type(img_obj) is Image)
     lines = cv2.HoughLinesP(masked_edges,
                             parm_dict['hough_rho'],
                             parm_dict['hough_theta'],
                             parm_dict['hough_min_intersect'],
                             parm_dict['hough_min_len'],
                             parm_dict['hough_max_gap'])
     return lines

tmp = iu.imRead("test_images/straight_lines2.jpg", reader='cv2', vwr=vwr)
lines = hough_lines(tmp, gpd)

vwr.show()
