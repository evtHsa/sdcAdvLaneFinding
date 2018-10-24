#fill!/usr/bin/env python3
#
# demo code, usually from the lesson excercise
# return images

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import pprint

#adapted from lesson 7.4 solution
class LaneBoundary:
    def __init__(self, init_x_current, img, bndry_title, vwr=None):
        assert(type(img) is iu.Image)
        assert(img.is2D())
        self.in_img = img
        _img_data = img.img_data
        self.out_img = iu.Image(img_data = np.dstack((_img_data, _img_data, _img_data)),
                           title = "lane pixels" + bndry_title)
        self.x = -1
        self.y = -1
        self.x_current = init_x_current
        self.ix_list = list()
        self.vwr = vwr #FIXME: should not be here, only 4 debug, remove l8r
        self.fit = None # just a note that we'll use this l8r
        self.ploty = None # just a note that we'll use this l8r
        self.parm_dict = None # set lazily on first window update
        
    def fit_polynomial(self):
        assert(type(self) is LaneBoundary)
        x = self.x
        y = self.y
        fit = np.polyfit(y, x, 2)
        ploty = np.linspace(0, self.in_img.img_data.shape[0] - 1,
                            self.in_img.img_data.shape[0])
        try:
            fit = fit[0] * ploty**2 + fit[1] * ploty + fit[2]
        except TypeError:
            # Avoids an error if fit is still none or incorrect
            print('fit_polynomal: failed to fit a line!')
            fit = 1*ploty**2 + 1*ploty
        assert(not fit is None)
        assert(not ploty is None)
        self.fit = fit
        self.ploty = ploty

    def fill_poly_points(self, flip):
        # we need to flip 1 of the lists of points to avoid the bowtie effect
        #
        # a bit more explanation:
        #    - we start with two linear arrays <fit> and <ploty> which are the x & y
        #      coordinates of the polynomial we fit to the lane pixels. so this looks like
        #      F = [1, 2, 3] P = [10, 20, 30]
        #    - vstack yields [[1, 2 3]
        #                           [11, 12, 13]]
        #    - transpose of that yields
        #      [[1, 11],
        #       [2, 12],
        #       [3, 13]]
        #    - now we just have to deal with the fact that both sets of points are in the same
        #    order so after drawing the bottom point of the first series we have a diagonal
        #    line to the top of the second series and another diagonal to close the polygon
        #    at the top of the first series(the "bowtie") so we flip one of the series of points
        assert(not self.fit is None)
        assert(not self.ploty is None)
        pts = np.vstack([self.fit, self.ploty]).T
        if flip:
            pts = np.flipud(pts)
        return np.array([pts])
    
    def concat_ixes(self):
        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        self.ix_list = np.concatenate(self.ix_list)
        
    def append_ixes(self):
        self.ix_list.append(self.window.good_ixes)

    def window_update(self, window):
        if self.parm_dict is None:
            self.parm_dict = window.parm_dict
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
        
    def show(self, title=None, verbose=False):
        if verbose:
            pprint.pprint(self.__dict__)
        else:
            print("%s Line\n\tx=%s\n\ty=%s," % (title, str(self.x), str(self.y)))
        
    def draw(self, img):
        assert(type(img) is iu.Image)
        iu.cv2Polylines(self.fit, self.ploty, img,
                        line_color = self.parm_dict['lane_line_color'],
                        line_thickness = self.parm_dict['lane_line_thickness'])

class Window:
    def __init__(self, img, win_ix, win_height, x_base, margin, vwr, nonzerox,
                 nonzeroy,parm_dict = None):
        assert(type(img) is iu.Image)
        self.y_lo = img.img_data.shape[0] - (win_ix + 1) * win_height
        self.y_hi = img.img_data.shape[0] - win_ix  * win_height
        self.x_lo = x_base - margin
        self.x_hi = x_base + margin
        self.ix = win_ix
        self.vwr = vwr
        self.good_ixes = ((nonzeroy >= self.y_lo) & (nonzeroy <= self.y_hi) &
                          (nonzerox >= self.x_lo) & (nonzerox <= self.x_hi)).nonzero()[0]
        self.parm_dict = parm_dict

    def print(self):
        print("win_%s: ix = %d y_lo = %d, y_hi = %d, x_lo = %d, x_hi = %d" %
              (self.title, self.ix, self.y_lo, self.y_hi, self.x_lo, self.x_hi))

    def draw(self, out_img):
        assert(type(out_img) is iu.Image)
        cv2.rectangle(out_img.img_data, (self.x_lo, self.y_lo), (self.x_hi, self.y_hi),
                      self.parm_dict['sliding_window_color'], 2)
class Lane:
    # for right now Lanes exist to hold a left and a right boundary and some misc
    # parm and cache dicts.
    def __init__(self, cd=None, pd=None, vwr=None):
        self.cd = cd
        self.pd = pd
        self.vwr = vwr
        self.left_bndry = None
        self.right_bndry = None
        
    def get_image(self, img):
        assert(type(img) is iu.Image)

        pts = np.hstack((self.left_bndry.fill_poly_points(True),
                         self.right_bndry.fill_poly_points(False)))

        out_img = iu.Image(img_data = np.zeros_like(img.img_data).astype(np.uint8),
                           title = "lane image", img_type = 'rgb')
        cv2.fillPoly(out_img.img_data, np.int_([pts]), self.pd['lane_fill_color'])
        self.left_bndry.draw(out_img)
        self.right_bndry.draw(out_img)
        iv._push(self.vwr, out_img)
        return out_img

    def fit_polynomials(self):
        self.left_bndry.fit_polynomial()
        self.right_bndry.fit_polynomial()

    def find_pixels_all_bndrys(self, binary_warped):
        assert(type(binary_warped) is iu.Image)
        assert(binary_warped.is2D())
    
        wp = self.pd['sliding_windows']
        nwindows, margin, minpix = (wp['nwindows'], wp['margin'], wp['minpix'])
        hist = iu.hist(binary_warped, self.vwr)
        left_max_ix, right_max_ix = iu.get_LR_hist_max_ix(hist)
        img_data = binary_warped.img_data #reduce typing

        # Set height of windows - based on nwindows above and image shape
        window_height = np.int(binary_warped.img_data.shape[0]//nwindows)

        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.img_data.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        # Current positions to be updated later for each window in nwindows
        self.left_bndry = LaneBoundary(left_max_ix, binary_warped, 'L', self.vwr)
        self.right_bndry = LaneBoundary(right_max_ix, binary_warped, 'R', self.vwr)

        for window in range(nwindows):
            for bndry in [self.left_bndry, self.right_bndry]:
                win = Window(binary_warped, window, window_height, bndry.x_current,
                             margin, self.vwr, nonzerox, nonzeroy, self.pd)
                # ok to here, good ixes on prev line
                bndry.window_update(win)
                bndry.draw_window(bndry.out_img) #FIXME: reference to image is redundant
                bndry.append_ixes()

                # If you found > minpix pixels, recenter next window on their mean position
                if len(bndry.window.good_ixes) > minpix:
                    bndry.x_current = np.int(np.mean(
                        nonzerox[bndry.window.good_ixes]))
                    # x_current is updated correctly
        self.left_bndry.finis(nonzerox, nonzeroy)
        self.right_bndry.finis(nonzerox, nonzeroy)


    
