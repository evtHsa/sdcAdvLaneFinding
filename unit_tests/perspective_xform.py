#!/usr/bin/env python3

# https://www.scivision.co/numpy-image-bgr-to-rgb/

import util as ut
import ImgViewer as iv
import ImgSaver as iS
import ImgUtil as iu

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']

def test_undistort(vwr, max_files):

    for fname in ut.get_fnames("test_images/", "test*.jpg", max_files):
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


