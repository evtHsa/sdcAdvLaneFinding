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
    def __init__(self, init_x_current, img):
        assert(type(img) is iu.Image)
        self.img = img
        self.x = -1
        self.y = -1
        self.x_current = init_x_current
        self.ix_list = list()
        
    def concat_ixes(self):
        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        self.ix_list = np.concatenate(self.ix_list)
        
    def append_ixes(self):
        self.ix_list.append(self.window.good_ixes)

    def window_update(self, window):
        self.window = window
        
    def draw_window(self, img):
        assert(type(img) is iu.Image)
        self.window.draw(out_img)
        
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
        assert(type(img) is iu.Image)
        ut.oneShotMsg("FIXME: rectangle colors and thickness shdb in parms")
        cv2.rectangle(out_img.img_data, (self.x_lo, self.y_lo), (self.x_hi, self.y_hi),
                      (0, 255, 0), 2)
        #FIXME:self.vwr.show_immed_ndarray(img = out_img, title = self.title,
        #                                 img_type = 'bgr')

def get_binary_warped_image_v2(path="", cd=None, pd=None, vwr=None):
    img = iu.imRead(path, reader='cv2', vwr=None)
    undistorted = iu.undistort(img, cd, vwr=None)
    top_down = iu.look_down(undistorted, cd, vwr)
    hls_lab = iu.hls_lab_lane_detect(top_down, cache_dict = cd, parm_dict = pd)
    
def get_binary_warped_image(path="", cd=None, pd=None, vwr=None):
    img = iu.imRead(path, reader='cv2', flags = cv2.IMREAD_GRAYSCALE, vwr=None)
    iv._push(vwr, img)
    return img
    
def find_lane_pixels(binary_warped_image, cd=None, pd=None, vwr=None):
    assert(type(binary_warped_image) is iu.Image)
    assert(binary_warped_image.is2D())
    
    wp = pd['sliding_windows']
    nwindows, margin, minpix = (wp['nwindows'], wp['margin'], wp['minpix'])
    hist = iu.hist(binary_warped_image, vwr)
    left_max_ix, right_max_ix = iu.get_LR_hist_max_ix(hist)
    img_data = binary_warped_image.img_data
    out_img = iu.Image(img_data = np.dstack((img_data, img_data, img_data)),
                       title="find_lane_pixels", img_type='gray')

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
        for lane in ['L', 'R']:
            win = Window(binary_warped, window, window_height, lanes['L'].x_current,
                         margin, "L", vwr, nonzerox, nonzeroy)
            lanes[lane] .window_update(win)
            lanes[lane].draw_window(out_img)
            lanes[lane].append_ixes()

            # If you found > minpix pixels, recenter next window on their mean position
            if len(lanes[lane].window.good_ixes) > minpix:
                lanes[lane].x_current = np.int(np.mean(
                    nonzerox[lanes[lane].window.good_ixes]))

    lanes['L'].finis(nonzerox, nonzeroy)
    lanes['R'].finis(nonzerox, nonzeroy)

    return lanes['L'], lanes['R'], out_img

def fit_polynomial(lane):
    x = lane.x
    ut.brk("FIXME:mine:do we agree with 7.4")
    y = lane.y
    fit = np.polyfit(y, x, 2)
    ploty = np.linspace(0, lane.img.shape[0] - 1, lane.img.shape[0])
    try:
        fit = fit[0] * ploty**2 + fit[1] * ploty + fit[2]
    except TypeError:
        # Avoids an error if `left` and `right_fit` are still none or incorrect
        print('fit_polynomal: failed to fit a line!')
        fit = 1*ploty**2 + 1*ploty
    lane.img  = [255, 0, 0]
    print("FIXME:??: where exactly is plot drawing, how do we return that image")
    plt.plot(fit, ploty, color='yellow')


def doit(path="", cd=None, pd=None, vwr=None):
    vwr.flush()
    for path in ut.get_fnames("test_images/", "*.jpg"):
        lane_L, lane_R, img = find_lane_pixels(path, cd, pd, vwr)
        lane_L.show(path + 'L')
        lane_R.show(path + 'R')
        iv._push(vwr, iu.Image(img_data=img, title = "sliding winders"))
    vwr.show()

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']
doit(cd=cache_dict, pd=parm_dict, vwr=vwr)

