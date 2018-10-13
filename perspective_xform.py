#!/usr/bin/env python3

# https://www.scivision.co/numpy-image-bgr-to-rgb/

import util as ut
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip
import ImgViewer as iv
import ImgSaver as iS
import ImgUtil as iu
from collections import deque
import parm_dict as pd

parm_dict = pd.parm_dict
cache_dict = pd.cache_dict

#saver = iS.ImgSaver()
saver = None

vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)

ut.cb_corners(parm_dict, cache_dict, max_files=0, verbose=False,
              vwr=None) #(obj,img)_points in cache
iu.calibrateCamera(parms=parm_dict, cache = cache_dict, vwr=vwr)
# now have mtx and dist in cache
iu.getLookDownXform(cache_dict) # cache['M_lookdown[_inv]']

def test_undistort(vwr, max_files):

    for fname in get_fnames("test_images/", "test*.jpg", max_files):
        img = iu.imRead(fname, reader='cv2', vwr=vwr)
        img = iu.undistort(img, cache_dict, vwr)
        iv._push_deprecated(vwr, img, title="undist", type="FIXME:shd come from img via imread")
    
#test_undistort(vwr, max_files=3)

def test_look_down(path, cache, vwr=None):
    iv._flush(vwr)
    img = iu.imRead(path, reader='cv2', vwr=vwr)
    img = iu.undistort(img, cache_dict, vwr)
    top_down = iu.look_down(img, cache, vwr)
    iv._show(vwr, clear=True)

def _test_look_down(cache, vwr):
    test_look_down("test_images/test1.jpg", cache, vwr=vwr)
    test_look_down("test_images/test3.jpg", cache, vwr=vwr)
    test_look_down("test_images/test5.jpg", cache, vwr=vwr)
    
_test_look_down(cache_dict, vwr)


