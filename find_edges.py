#!/usr/bin/env python3

import util as ut
import demo
import  cv2
import ImgSaver as iS
import ImgUtil as iu
import ImgViewer as iv
import glob
import parm_dict as pd

parm_dict = pd.parm_dict
cache_dict = pd.cache_dict

#saver = iS.ImgSaver()
saver = None

vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)
fname_list = glob.glob("camera_cal/*.jpg")

ut.cb_corners(parm_dict, cache_dict, max_files=0, verbose=False,
              vwr=None) #(obj,img)_points in cache
iu.calibrateCamera(parms=parm_dict, cache = cache_dict, vwr=vwr)
# now have mtx and dist in cache

tmp = iu.img_read("test_images/straight_lines2.jpg", vwr) # walk first then...


vwr.show()
