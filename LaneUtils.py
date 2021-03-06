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
from moviepy.editor import VideoFileClip
import parm_dict as pd

class LaneBoundary:
    
    def __init__(self,  init_x_current, img, bndry_title, lane = None, vwr=None):
        ut._assert(type(img) is iu.Image)
        ut._assert(img.is2D())
        ut._assert(type(lane) is Lane)
        
        ut._assert(not lane is None)
        self.lane = lane # our parent so we can reference attrs common to all lanes
        self.in_img = img
        _img_data = img.img_data
        self.out_img = iu.Image(img_data = np.dstack((_img_data, _img_data, _img_data)),
                           title = "lane pixels" + bndry_title)
        self._x = -1
        self._y = -1
        self.x_current = init_x_current
        self.ix_list = list()
        self.vwr = vwr #FIXME: should not be here, only 4 debug, remove l8r
        self.title = bndry_title
        self.fit_x = None # just a note that we'll use this l8r
        self.parm_dict = None # set lazily on first window update

    def set_x(self, x):
        ut._assert(len(x) != 0)
        self._x = x
        
    def get_x(self):
        return self._x

    def set_y(self, y):
        self._y = y
        
    def get_y(self):
        return self._y

    def radius_of_curvature_p(self):
        #FIXME: obsolete fn but leave it about for a while 102718
        fitc = self.fit_coeff
        y = self.lane.ploty
        y_eval = np.max(y)
        ret   = ((1 + (2*fitc[0]*y_eval + fitc[1])**2)**1.5) / np.absolute(2*fitc[0])
        return ret
        
    def radius_of_curvature_m(self):
        x = self.get_x()
        y = self.get_y()
        y_eval = np.max(y)
        xmpp = self.lane.pd['xm_per_pix']
        ympp = self.lane.pd['ym_per_pix']
        fitc = np.polyfit(y*ympp, x*xmpp, 2)
        ret  =  ((1 + (2*fitc[0]*y_eval*ympp
                                     + fitc[1])**2)**1.5) / np.absolute(2*fitc[0])
        return ret
        
    def fit_polynomial(self):
        # return false on fail
        x = self.get_x()
        y = self.get_y()
        xmpp = self.lane.pd['xm_per_pix']
        ympp = self.lane.pd['ym_per_pix']
        ploty = self.lane.ploty # from our owning lane
        ut._assert(not ploty is None)
        try:
            self.fit_coeff = np.polyfit(y, x, 2)
        except Exception as ex:
            print("FIXME:%s lane boundry polyfit failed: %s" % (self.title,
                                                           ut.format_exception(ex)))
            return False
        try:
            self.fit_x = self.fit_coeff[0] * ploty**2 + self.fit_coeff[1] * ploty + self.fit_coeff[2]
        except TypeError:
            # Avoids an error if fit is still none or incorrect
            print('fit_polynomal: failed to fit a line!')
            self.fit_x = 1*ploty**2 + 1*ploty
            return False

        ut._assert(not self.fit_x is None)
        return True

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
        ut._assert(not self.fit_x is None)
        ploty = self.lane.ploty # from our owning lane
        ut._assert(not ploty is None)
        pts = np.vstack([self.fit_x, ploty]).T
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
        ut._assert(type(img) is iu.Image)
        self.window.draw(img)
        
    def finis(self, nonzerox, nonzeroy):
        try:
            self.concat_ixes()
        except Exception as ex:
            # Avoids an error if the above is not implemented fully
            ut.brk("%s.finis => %s" % (self.title, ut.format_exception(ex)))
            pass
        self.set_x(nonzerox[self.ix_list])
        self.set_y(nonzeroy[self.ix_list])
        
    def show(self, title=None, verbose=False):
        if verbose:
            pprint.pprint(self.__dict__)
        else:
            print("%s Line\n\tx=%s\n\ty=%s," % (title, str(self.get_x()),
                                                str(self.get_y())))
        
    def draw(self, img):
        ut._assert(type(img) is iu.Image)
        ploty = self.lane.ploty # from our owning lane
        ut._assert(not ploty is None)
        iu.cv2Polylines(self.fit_x, ploty, img,
                        line_color = self.parm_dict['lane_line_color'],
                        line_thickness = self.parm_dict['lane_line_thickness'])

class Window:
    def __init__(self, img, win_ix, win_height, x_base, margin, vwr, nonzerox,
                 nonzeroy,parm_dict = None):
        ut._assert(type(img) is iu.Image)
        self.y_lo = img.img_data.shape[0] - (win_ix + 1) * win_height
        self.y_hi = img.img_data.shape[0] - win_ix  * win_height
        self.x_lo = x_base - margin
        self.x_hi = x_base + margin
        self.ix = win_ix
        self.vwr = vwr
        self.good_ixes = ((nonzeroy >= self.y_lo) &
                          (nonzeroy <= self.y_hi) &
                          (nonzerox >= self.x_lo) &
                          (nonzerox <= self.x_hi)).nonzero()[0]
        self.parm_dict = parm_dict

    def print(self, msg=""):
        print("win_%s: ix = %d y_lo = %d, y_hi = %d, x_lo = %d, x_hi = %d" %
              (msg, self.ix, self.y_lo, self.y_hi, self.x_lo, self.x_hi))

    def draw(self, out_img):
        ut._assert(type(out_img) is iu.Image)
        cv2.rectangle(out_img.img_data, (self.x_lo, self.y_lo), (self.x_hi, self.y_hi),
                      self.parm_dict['sliding_window_color'], 2)
class Lane:
    # for right now Lanes exist to hold a left and a right boundary and some misc
    # parm and cache dicts.
    def __init__(self, cd=None, pd=None, vwr=None,
                 binary_warper=iu.FIXME_lane_detect):
        ut._assert(not cd is  None)
        ut._assert(not pd is None)
        #vwr may be None
        self.cd = cd
        self.pd = pd
        self.vwr = vwr
        self.left_bndry = None
        self.right_bndry = None
        self.FIXME_stage = None
        self.binary_warper = binary_warper
        self.last_pipe_stage = None
        self.sum_lane_widths = 0

    def display_curve_rad(self):
        lrc = self.left_bndry.radius_of_curvature_m()
        rrc = self.right_bndry.radius_of_curvature_m()
        avg_roc = (lrc + rrc) / 2
        ret = "curvature radius = %.2f m" % avg_roc
        return ret
    
    def note_img_attrs(self, img=None):
        self.height, self.width, self.num_chan = img.img_data.shape
        self.ploty = np.linspace(0, img.img_data.shape[0] - 1, img.img_data.shape[0])

    def log_stage(self, img=None, stwing=""):
        tmp = stwing
        if img:
            assert(not img.title == "")
            tmp= img.title
            if self.vwr and self.vwr.svr:
                self.vwr.svr.save(img)
            
        assert(not tmp == "")
        self.last_pipe_stage = tmp
        #print("log_stage:%s" % tmp)
        self.FIXME_state = tmp

        
    def lane_finder_pipe(self, in_img, cd=None, pd=None, vwr=None):
        # return processed image or None on error
        try:
            ut._assert(not in_img is None)
            ut._assert(type(in_img) is iu.Image)
            self.note_img_attrs(in_img)
            self.log_stage(in_img)
            
            undistorted = iu.undistort(in_img, cd, vwr=vwr)
            self.log_stage(undistorted)
            top_down = iu.look_down(undistorted, cd, vwr)
            self.log_stage(top_down)
            binary_warped = self.binary_warper(top_down, cache_dict = cd,
                                               parm_dict = pd)
            self.log_stage(binary_warped)
            self.find_pixels_all_bndrys(binary_warped)
            if not self.fit_polynomials():
                return None
            lane_img = self.get_image(in_img)
            self.log_stage(lane_img)
            size = (lane_img.shape()[1], lane_img.shape()[0])
            lane_img = iu.cv2WarpPerspective(lane_img, cd['M_lookdown_inv'], size,
                                             vwr=vwr)
            self.log_stage(lane_img, 'rewarped_lane_img')
            blended_img = iu.cv2AddWeighted(in_img, lane_img,
                                            alpha = pd['lane_blend_alpha'],
                                            beta = pd['lane_blend_beta'],
                                            gamma = pd['lane_blend_gamma'], title = "merged")
            self.log_stage(blended_img)
            self.calc_vehicle_pos()
            blended_img.msgs = []
            blended_img.msgs.append(self.display_vehicle_pos())
            blended_img.msgs.append(self.display_curve_rad())
            blended_img.putText()
            blended_img.title = 'annotated_blended_img'
            self.log_stage(blended_img)
            return blended_img
        except Exception as ex:
            print("FIXME:%s" % ut.format_exception(ex))
            return None
        
    def get_image(self, img): #FIXME: name not at all evocative of purpose
        ut._assert(type(img) is iu.Image)

        pts = np.hstack((self.left_bndry.fill_poly_points(True),
                         self.right_bndry.fill_poly_points(False)))

        out_img = iu.Image(img_data = np.zeros_like(img.img_data).astype(np.uint8),
                           title = "lane_image", img_type = 'rgb')
        cv2.fillPoly(out_img.img_data, np.int_([pts]), self.pd['lane_fill_color'])
        self.left_bndry.draw(out_img)
        self.right_bndry.draw(out_img)
        return out_img

    def display_vehicle_pos(self):
        ret = "%.2f meters %s of center" % (
            np.abs(self.vehicle_pos), self.pos_w_r_t_lane_ctr)
        return ret
        
    def calc_vehicle_pos(self):
        pic_ctr = self.width / 2
        x_l = self.left_bndry.get_x()[0]
        x_r = self.right_bndry.get_x()[0]
        ut._assert(x_l < x_r)
        lane_ctr = x_l + (x_r - x_l)/2
        self.vehicle_pos = (pic_ctr - lane_ctr) * self.pd['xm_per_pix']
        self.pos_w_r_t_lane_ctr = "left" if pic_ctr < lane_ctr else "right"
        self.sum_lane_widths += x_r - x_l

    def fit_polynomials(self):
        # return false if neither fits
        #ut.brk("hey?>")
        lpf = self.left_bndry.fit_polynomial()
        rpf = self.right_bndry.fit_polynomial()
        return lpf and rpf

    def find_pixels_all_bndrys(self, binary_warped):
        ut._assert(type(binary_warped) is iu.Image)
        ut._assert(binary_warped.is2D())
    
        wp = self.pd['sliding_windows']
        nwindows, margin, minpix = (wp['nwindows'],
                                    wp['margin'], wp['minpix'])
        hist = iu.hist(binary_warped)
        # log stage needs a bigger brain to display 2d histograms than the current code has
        #self.log_stage(hist)
        left_max_ix, right_max_ix = iu.get_LR_hist_max_ix(hist)
        #print("hist maxima L, R = %d, %d" % (left_max_ix, right_max_ix))
        #iv.plt.plot(hist) # FIXME
        #iv.plt.show() # FIXME
        img_data = binary_warped.img_data #reduce typing

        # Set height of windows - based on nwindows above and image shape
        window_height = np.int(binary_warped.img_data.shape[0]//nwindows)

        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.img_data.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        # Current positions to be updated later for each window in nwindows
        self.left_bndry = LaneBoundary(left_max_ix, binary_warped, 'L', lane=self,
                                       vwr=self.vwr)
        self.right_bndry = LaneBoundary(right_max_ix, binary_warped, 'R', lane = self,
                                        vwr=self.vwr)

        for window in range(nwindows):
            for bndry in [self.left_bndry, self.right_bndry]:
                win = Window(binary_warped, window, window_height, bndry.x_current,
                             margin, self.vwr, nonzerox, nonzeroy, self.pd)
                # ok to here, good ixes on prev line
                bndry.window_update(win)
                #FIXME: reference to image is redundant
                bndry.draw_window(bndry.out_img) 
                bndry.append_ixes()

                # If you found > minpix pixels, recenter next window on
                # their mean position
                if len(bndry.window.good_ixes) > minpix:
                    bndry.x_current = np.int(np.mean(
                        nonzerox[bndry.window.good_ixes]))
        self.left_bndry.finis(nonzerox, nonzeroy)
        self.right_bndry.finis(nonzerox, nonzeroy)
        
class VideoCtrlr:
    def __init__(self, basename, viewer=False, saver=False, binary_warper=None):
        self.frame_ctr = 0
        self.faulty_frames = 0
        self.cache_dict, self.parm_dict = ut.app_init(viewer=viewer, saver=saver,
                                                       title="whatever")
        self.vwr = None
        if viewer:
            self.vwr = self.cache_dict['viewer']
            # we create them for video debug but even  then only turn them
            # on when needed
            self.vwr.bce_set_enabled(False)
        self.lane = Lane(self.cache_dict, self.parm_dict, vwr=self.vwr,
                         binary_warper=binary_warper)
        in_path = basename + ".mp4"
        print("processing " + in_path)
        out_path = ut.get_out_dir() + basename + ".mp4"
        video_in = VideoFileClip(in_path)
        rendered_video = video_in.fl_image(self.process_frame_bp)
        rendered_video.write_videofile(out_path, audio=False)
        print("average lane width = %f" % (self.lane.sum_lane_widths / self.frame_ctr))
        if self.faulty_frames:
            print("\n\n Total Frames %d, failed to find lane boundaries in %d frames"
                  % (self.frame_ctr, self.faulty_frames))
        
    def process_frame(self, img_data):
        # FIXME: es ware besser wenn unser pipeline nativ mit RGB arbeitet
        img = iu.Image(img_data = img_data, title="", img_type='rgb')
        bgr_img = iu.cv2CvtColor(img, cv2.COLOR_RGB2BGR)
        pipe_out_img = self.lane.lane_finder_pipe(bgr_img, self.cache_dict,
                                                  self.parm_dict, self.vwr)
        ret_img = iu.cv2CvtColor(pipe_out_img, cv2.COLOR_BGR2RGB)
        self.frame_ctr += 1
        return ret_img.img_data

    def process_frame_bp(self, img_data):
        # FIXME: es ware besser wenn unser pipeline nativ mit RGB arbeitet
        bad_frame_list = pd.parm_dict['bad_frame_ixes']
        bummer = False
        img = iu.Image(img_data = img_data, title="", img_type='rgb')
        bgr_img = iu.cv2CvtColor(img, cv2.COLOR_RGB2BGR)
        if bad_frame_list.count(self.frame_ctr):
            bummer = True
            print("WHOO HOOO: logging stuff for frame %d" % self.frame_ctr)
            self.bce_set_enabled(bummer)
            ut.brk("dig in bubba")
        pipe_out_img = self.lane.lane_finder_pipe(bgr_img, self.cache_dict,
                                                  self.parm_dict, self.vwr)
        if bummer:
            bummer = False
            self.bce_set_enabled(bummer)
            
        if pipe_out_img == None:
            print("\ncould not find lane boundaries in frame %d\n" % (self.frame_ctr))
            self.faulty_frames += 1
            img.title = "badFrame_"+str(self.frame_ctr)+".jpg"
            if self.vwr and self.vwr.svr:
                self.vwr.svr.save(img)
            ret_img = img
        else:
            ret_img = iu.cv2CvtColor(pipe_out_img, cv2.COLOR_BGR2RGB)
        self.frame_ctr += 1
        if self.faulty_frames:
            ut._quit("my dreams are shattered, i quit")
        return ret_img.img_data
    
    def bce_set_enabled(self, enabled):
        if self.vwr:
            self.vwr.bce_set_enabled(enabled) #"bce" means "everything" in russian
