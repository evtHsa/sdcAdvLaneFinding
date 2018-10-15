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
        #iv._push(vwr, img)
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']

#combined_hls_lab = iu.hls_lab_line_detect('test_images/bridge_shadow.jpg',
#                                          cache_dict = cache_dict, parm_dict = parm_dict)
#iv._push(vwr, combined_hls_lab)

doit(cd=cache_dict, pd=parm_dict, vwr=vwr)
