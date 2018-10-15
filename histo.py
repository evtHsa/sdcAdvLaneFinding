#!/usr/bin/env python3
#
# demo code, usually from the lesson excercise
# return images

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu

# for some bizzare reason, the image in the lesson, which I cant download,
# results in an n x m image, not n x m x 3
def hist(img, vwr):
    assert(type(img) is Image)
    ut.brk("step by step")
    # Lane lines are likely to be mostly vertical nearest to the car
    
    bottom_half = img.img_data[img.shape[0]//2:,:]
    
    # TO-DO: Sum across image pixels vertically - make sure to set `axis`
    # i.e. the highest areas of vertical lines should be larger values
    histogram = np.sum(bottom_half, axis=0)
    print("bottom_half.shape = " + str(bottom_half.shape))
    print("gray.shape = " + str(gray.shape))
    print("histogram.shape = " + str(histogram.shape))
    iv._push(vwr,
             iu.Image(img_data = histogram, title="histo??", type='gray'))
    ut.brk("that's all folx")
    return histogram

def histo_pipe(path="", cd=None, pd=None, vwr=None):
    ut.oneShotMsg("FIXME: this probably should move to ImgUtil")
    img = iu.imRead(path, reader='cv2', vwr=None)
    iv._push(vwr,img) # initial img
    undistorted = iu.undistort(img, cd, vwr=None)
    top_down = iu.look_down(undistorted, cd, None)
    hls_lab = iu.hls_lab_line_detect(top_down, cache_dict = cd, parm_dict = pd)
    ret = hist(hls_lab, vwr)
    iv._push(vwr,ret) # result img
    return ret
    
def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    for path in ut.get_fnames("test_images/", "*.jpg"):
        img = histo_pipe(path, cd, pd, vwr)
        #iv._push(vwr, img)
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']
doit(cd=cache_dict, pd=parm_dict, vwr=vwr)

