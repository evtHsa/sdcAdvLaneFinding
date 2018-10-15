#!/usr/bin/env python3
#
# demo code, usually from the lesson excercise
# return images

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import matplotlib.pyplot as plt

def sliding_windows_pipe(path="", cd=None, pd=None, vwr=None):
    # FIXME: subsume from tmp.py from 7.4 solution to here
    wp = pd['sliding_windows']
    nwindows, margin, minpix = (wp['nwindows'], wp['margin'], wp['minpix'])
    img = iu.imRead(path, reader='cv2', vwr=None)
    undistorted = iu.undistort(img, cd, vwr=None)
    top_down = iu.look_down(undistorted, cd, vwr)
    hls_lab = iu.hls_lab_lane_detect(top_down, cache_dict = cd, parm_dict = pd)
    hist = iu.hist(hls_lab, vwr)
    left_max_ix, right_max_ix = iu.get_LR_hist_max_ix(hist)
    print("FIXME: histo maxen = %d, %d" % (left_max_ix, right_max_ix))
    ut.brk("look what a fine mess you've got us into know ollie")
  
def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    for path in ut.get_fnames("test_images/", "*.jpg"):
        sliding_windows_pipe(path, cd, pd, vwr)
        ut.brk('what ed koch said')
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']
doit(cd=cache_dict, pd=parm_dict, vwr=vwr)

