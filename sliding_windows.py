#!/usr/bin/env python3
#
# demo code, usually from the lesson excercise
# return images

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import matplotlib.pyplot as plt #FIXME: nuke?
import ImgViewer as iv

#adapted from lesson 7.4 solution
class Lane:
    def __init__(self, init_x_current):
        self.x = -1
        self.y = -1
        self.x_current = init_x_current
        self.ix_list = list()
        
    def concat_ixes(self):
        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        self.ix_list = np.concatenate(self.ix_list)
        
    def append_ixes(self, ixes):
        self.ix_list.append(ixes)
        
class Window:
    def __init__(self, img, win_ix, win_height, x_base, margin, title, vwr, nonzerox,
                 nonzeroy):
        assert(type(img) is np.ndarray)
        self.y_lo = img.shape[0] - (win_ix + 1) * win_height
        self.y_hi = img.shape[0] - win_ix  * win_height
        self.x_lo = x_base - margin
        self.x_hi = x_base + margin
        self.ix = win_ix
        self.title = title
        self.vwr = vwr
        self.good_ixes = ((nonzeroy >= self.y_lo) & (nonzeroy <= self.y_hi) &
                          (nonzerox >= self.x_lo) & (nonzerox <= self.x_hi)).nonzero()[0]

    def print(self):
        print("win_%s: ix = %d y_lo = %d, y_hi = %d, x_lo = %d, x_hi = %d" %
              (self.title, self.ix, self.y_lo, self.y_hi, self.x_lo, self.x_hi))

    def draw(self, out_img):
        ut.oneShotMsg("FIXME: rectangle colors and thickness shdb in parms")
        cv2.rectangle(out_img, (self.x_lo, self.y_lo), (self.x_hi, self.y_hi),
                      (0, 255, 0), 2)
        #FIXME:self.vwr.show_immed_ndarray(img = out_img, title = self.title,
        #                                 img_type = 'bgr')
        
def find_lane_pixels(path="", cd=None, pd=None, vwr=None):
    # FIXME: subsume from tmp.py from 7.4 solution to here
    wp = pd['sliding_windows']
    nwindows, margin, minpix = (wp['nwindows'], wp['margin'], wp['minpix'])
    img = iu.imRead(path, reader='cv2', vwr=None)
    undistorted = iu.undistort(img, cd, vwr=None)
    top_down = iu.look_down(undistorted, cd, vwr)
    hls_lab = iu.hls_lab_lane_detect(top_down, cache_dict = cd, parm_dict = pd)
    hist = iu.hist(hls_lab, vwr)
    left_max_ix, right_max_ix = iu.get_LR_hist_max_ix(hist)

    binary_warped = hls_lab.img_data # re-use code w/less typing
    out_img = np.dstack((binary_warped, binary_warped, binary_warped))

    # Set height of windows - based on nwindows above and image shape
    window_height = np.int(binary_warped.shape[0]//nwindows)

    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    # Current positions to be updated later for each window in nwindows
    lanes =  { 'L' : Lane(left_max_ix), 'R': Lane(right_max_ix)}
    
    for window in range(nwindows):
        win_L = Window(binary_warped, window, window_height, lanes['L'].x_current,
                       margin, "L", vwr, nonzerox, nonzeroy)
        win_L.draw(out_img)
        win_R = Window(binary_warped, window, window_height, lanes['R'].x_current,
                       margin, "R", vwr, nonzerox, nonzeroy)
        win_R.draw(out_img)

        lanes['L'].append_ixes(win_L.good_ixes)
        lanes['R'].ix_list.append(win_R.good_ixes)

        # If you found > minpix pixels, recenter next window on their mean position
        if len(win_L.good_ixes) > minpix:
            lanes['L'].x_current = np.int(np.mean(nonzerox[win_L.good_ixes]))
        if len(win_R.good_ixes) > minpix:        
            lanes['R'].x_current = np.int(np.mean(nonzerox[win_R.good_ixes]))

    # Concatenate the arrays of indices (previously was a list of lists of pixels)
    try:
        lanes['L'].concat_ixes()
        lanes['R'].concat_ixes()
    except ValueError:
        # Avoids an error if the above is not implemented fully
        pass

    # Extract left and right line pixel positions
    leftx = nonzerox[lanes['L'].ix_list]
    lefty = nonzeroy[lanes['L'].ix_list]
    rightx = nonzerox[lanes['R'].ix_list]
    righty = nonzeroy[lanes['R'].ix_list]

    return leftx, lefty, rightx, righty, out_img

def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    for path in ut.get_fnames("test_images/", "*.jpg"):
        lx, ly, rx, ry, img = find_lane_pixels(path, cd, pd, vwr)
        iv._push(vwr, iu.Image(img_data=img, title = "sliding winders"))
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']
doit(cd=cache_dict, pd=parm_dict, vwr=vwr)

