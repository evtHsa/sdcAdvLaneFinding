#!/usr/bin/env python3
#
# demo code, usually from the lesson excercise
# return images

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv

#adapted from lesson 7.4 solution
class Lane:
    def __init__(self, init_x_current, img, color_rgb, lane_title, vwr=None):
        assert(type(img) is iu.Image)
        assert(img.is2D())
        self.in_img = img
        _img_data = img.img_data
        self.out_img = iu.Image(img_data = np.dstack((_img_data, _img_data, _img_data)),
                           title = "lane pixels" + lane_title)
        self.x = -1
        self.y = -1
        self.x_current = init_x_current
        self.ix_list = list()
        self.color_rgb = color_rgb
        self.vwr = vwr #FIXME: should not be here, only 4 debug, remove l8r
        self.fit = None # just a note that we'll use this l8r
        self.ploty = None # just a note that we'll use this l8r

    def concat_ixes(self):
        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        self.ix_list = np.concatenate(self.ix_list)
        
    def append_ixes(self):
        self.ix_list.append(self.window.good_ixes)

    def window_update(self, window):
        self.window = window
        
    def draw_window(self, img):
        assert(type(img) is iu.Image)
        self.window.draw(img)
        
    def finis(self, nonzerox, nonzeroy):
        try:
            self.concat_ixes()
        except:
            # Avoids an error if the above is not implemented fully
            pass
        self.x = nonzerox[self.ix_list]
        self.y = nonzeroy[self.ix_list]
        
    def show(self, title):
        print("%s Line\n\tx=%s\n\ty=%s," % (title, str(self.x), str(self.y)))
        
class Window:
    def __init__(self, img, win_ix, win_height, x_base, margin, title, vwr, nonzerox,
                 nonzeroy,parm_dict = None):
        assert(type(img) is iu.Image)
        self.y_lo = img.img_data.shape[0] - (win_ix + 1) * win_height
        self.y_hi = img.img_data.shape[0] - win_ix  * win_height
        self.x_lo = x_base - margin
        self.x_hi = x_base + margin
        self.ix = win_ix
        self.title = title
        self.vwr = vwr
        self.good_ixes = ((nonzeroy >= self.y_lo) & (nonzeroy <= self.y_hi) &
                          (nonzerox >= self.x_lo) & (nonzerox <= self.x_hi)).nonzero()[0]
        self.parm_dict = parm_dict

    def print(self):
        print("win_%s: ix = %d y_lo = %d, y_hi = %d, x_lo = %d, x_hi = %d" %
              (self.title, self.ix, self.y_lo, self.y_hi, self.x_lo, self.x_hi))

    def draw(self, out_img):
        assert(type(out_img) is iu.Image)
        ut.oneShotMsg("FIXME: rectangle colors and thickness shdb in parms")
        cv2.rectangle(out_img.img_data, (self.x_lo, self.y_lo), (self.x_hi, self.y_hi),
                      self.parm_dict['sliding_window_color'], 2)

def find_lane_pixels(binary_warped, cd=None, pd=None, vwr=None):
    assert(type(binary_warped) is iu.Image)
    assert(binary_warped.is2D())
    
    wp = pd['sliding_windows']
    nwindows, margin, minpix = (wp['nwindows'], wp['margin'], wp['minpix'])
    hist = iu.hist(binary_warped, vwr)
    left_max_ix, right_max_ix = iu.get_LR_hist_max_ix(hist)
    img_data = binary_warped.img_data

    # Set height of windows - based on nwindows above and image shape
    window_height = np.int(binary_warped.img_data.shape[0]//nwindows)

    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.img_data.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    # Current positions to be updated later for each window in nwindows
    lanes =  {
        'L' : Lane(left_max_ix, binary_warped, pd['rgb']['red'], 'L', vwr),
        'R': Lane(right_max_ix, binary_warped, pd['rgb']['blue'], 'R', vwr)}
    
    for window in range(nwindows):
        for lane in ['L', 'R']:
            _lane = lanes[lane] # reduce typing
            win = Window(binary_warped, window, window_height, _lane.x_current,
                         margin, "L", vwr, nonzerox, nonzeroy, pd)
            # ok to here, good ixes on prev line
            _lane .window_update(win)
            _lane.draw_window(_lane.out_img)
            _lane.append_ixes()

            # If you found > minpix pixels, recenter next window on their mean position
            if len(_lane.window.good_ixes) > minpix:
                _lane.x_current = np.int(np.mean(
                    nonzerox[_lane.window.good_ixes]))
            # x_current is updated correctly
    lanes['L'].finis(nonzerox, nonzeroy)
    lanes['R'].finis(nonzerox, nonzeroy)
    return lanes

def fit_polynomial(lane, pd=None):
    assert(type(lane) is Lane)
    x = lane.x
    y = lane.y
    fit = np.polyfit(y, x, 2)
    ploty = np.linspace(0, lane.in_img.img_data.shape[0] - 1,
                        lane.in_img.img_data.shape[0])
    ut.oneShotMsg("FIXME:why are polyfit coefficients close but not identical")
    try:
        fit = fit[0] * ploty**2 + fit[1] * ploty + fit[2]
    except TypeError:
        # Avoids an error if fit is still none or incorrect
        print('fit_polynomal: failed to fit a line!')
        fit = 1*ploty**2 + 1*ploty
    lane.fit = fit
    lane.ploty = ploty
    lane.out_img.img_data[y,x]  = lane.color_rgb
    iu.cv2Polylines(fit, ploty, lane.out_img, line_color = pd['lane_line_color'],
                    line_thickness = pd['lane_line_thickness'])
    #iv._view(lane.vwr, img=lane.out_img, title="duh?")