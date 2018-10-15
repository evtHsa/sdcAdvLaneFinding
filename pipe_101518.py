#!/usr/bin/env python3

import util as ut
import ImgViewer as iv
import ImgUtil as iu
import cv2
import numpy as np
    
def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    for path in ut.get_fnames("test_images/", "*.jpg"):
        img = iu.hls_lab_pipeline(path, cd, pd, vwr)
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']

doit(cd=cache_dict, pd=parm_dict, vwr=vwr)
