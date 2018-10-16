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

#adapted from lesson 7.4 solution
class Window:
    def __init__(self, img, win_ix, win_height, x_base, margin, title):
        self.y_lo = img.shape[0] - (win_ix + 1) * win_height
        self.y_hi = img.shape[0] - win_ix  * win_height
        self.x_lo = x_base - margin
        self.x_hi = x_base + margin
        self.ix = win_ix
        self.title = title

    def print(self):
        print("win_%s: ix = %d y_lo = %d, y_hi = %d, x_lo = %d, x_hi = %d" %
              (self.title, self.ix, self.y_lo, self.y_hi, self.x_lo, self.x_hi))
        
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
    binary_warped = top_down.img_data # re-use code w/less typing

    # Set height of windows - based on nwindows above and image shape
    window_height = np.int(binary_warped.shape[0]//nwindows)
    print("FIXME: window_height = %d" % window_height)

    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    # Current positions to be updated later for each window in nwindows
    leftx_current = left_max_ix
    rightx_current = right_max_ix
    
    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []

    for window in range(nwindows):
        win_L = Window(binary_warped, window, window_height, leftx_current, margin, "L")
        win_L.print()
        win_R = Window(binary_warped, window, window_height, rightx_current, margin, "R")
        win_R.print()
        
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

