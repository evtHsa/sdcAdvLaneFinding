#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import LaneUtils as lu

# our object model
# Lanes:  contain LaneBoundary(s) and attributes common to both boundaries
# LaneBoundary(s): contain attributes for a particular lane bounday
# Windows: are used to calculate lane boundaries

#cd is cache_dict, pd is parm_dict
cd, pd = ut.app_init(viewer=True, saver=True, title="whatever")
cd['fit_units'] = 'pixels'
vwr = cd['viewer']

ut.oneShotMsg("FIXME: change pixels in prev line to meters")

vwr.flush()

for path in ut.get_fnames("test_images/", "*.jpg"):
    print("FIXME: path = %s" % path)
    in_img = iu.imRead(path, reader='cv2', vwr=None)
    lane = lu.Lane(cd, pd, img = in_img, units='pixels', vwr=None)
    ut.oneShotMsg("above is stupid, img shd not be in lane ctor")
    out_img= lane.lane_finder_pipe(in_img, cd, pd, vwr=vwr)
    iv._push(vwr, out_img)
    
vwr.show()
