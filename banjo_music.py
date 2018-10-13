#!/usr/bin/env python3

import util as ut
import demo
import  cv2
import ImgSaver as iS
import ImgUtil as iu
import ImgViewer as iv
import glob
import parm_dict as pd

parm_dict = pd.parm_dict
cache_dict = pd.cache_dict

#saver = iS.ImgSaver()
saver = None
vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)
fname_list = glob.glob("camera_cal/*.jpg")

ut.cb_corners(parm_dict, cache_dict, max_files=0, verbose=False,
              vwr=None) #(obj,img)_points in cache
iu.calibrateCamera(parms=parm_dict, cache = cache_dict, vwr=vwr)
# now have mtx and dist in cache


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

#saver = iS.ImgSaver()
saver = None
vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)

tmp = iu.imRead("test_images/straight_lines2.jpg", reader='cv2', vwr=vwr)
lines = iu.hough_lines(tmp, gpd)

vwr.show()
