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

# for some bizzare reason, the image in the lesson, which I cant download,
# results in an n x m image, not n x m x 3
def hist(img, vwr):
    assert(type(img) is iu.Image)
    # Lane lines are likely to be mostly vertical nearest to the car
    
    bottom_half = img.img_data[img.img_data.shape[0]//2:,:]
    
    # Sum across image pixels vertically - make sure to set `axis`
    # i.e. the highest areas of vertical lines should be larger values
    histogram = np.sum(bottom_half, axis=0)
    histogram = iu.Image(img_data = histogram, title="", type='gray')
    return histogram

def histo_pipe(path="", cd=None, pd=None, vwr=None):
    ut.oneShotMsg("FIXME: this probably should move to ImgUtil")
    hls_lab = iu.hls_lab_pipeline(path, cd, pd, vwr)
    ret = hist(hls_lab, vwr)
    hist.title = "hist: " + path
    return ret
    
def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    for path in ut.get_fnames("test_images/", "*.jpg"):
        hist = histo_pipe(path, cd, pd, vwr)
        hist.title="hist: " + path
        iv._push(vwr, hist)
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']
doit(cd=cache_dict, pd=parm_dict, vwr=vwr)

