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

def analyze_hist(hist):
    # see lesson 7.4
    width = hist.img_data.shape[0]
    midway = width // 2
    
    left_max_ix    = np.argmax(hist.img_data[0:midway])
    right_max_ix = midway + np.argmax(hist.img_data[midway:width])
    print("histo maxen = %d, %d" % (left_max_ix, right_max_ix))
    
def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    for path in ut.get_fnames("test_images/", "*.jpg"):
        hist = iu.histo_pipe(path, cd, pd, vwr)
        hist.title="hist: " + path
        analyze_hist(hist)
        iv._push(vwr, hist)
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']
doit(cd=cache_dict, pd=parm_dict, vwr=vwr)

