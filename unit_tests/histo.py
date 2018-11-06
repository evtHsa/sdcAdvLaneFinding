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
    for path in ut.get_fnames("test_images/", "problem_binary_warped.jpg"):
        img = iu.imRead(path, flags = cv2.IMREAD_GRAYSCALE, reader='cv2',
                        vwr=None)
        ut.brk("wtf?")
        hist = iu.hist(img)
        ut.brk("plot the histogram")
        ut.brk("call get_LR_hist_max_ix()")
        iv._push(vwr, hist)
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']
ut.brk("this unit test is broken")
doit(cd=cache_dict, pd=parm_dict, vwr=vwr)



