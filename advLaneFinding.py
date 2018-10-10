#!/usr/bin/env python3

import util as ut
import demo
import  cv2
import ImgViewer as iv
import ImgSaver as iS
import glob

# FIXME: may want to tweak some of thse parms
# gpd -> global parm dict
gpd ={ 
    'chessboard_nx' : 9,
    'chessboard_ny' : 6,
    'objpoints' : [],
    'imgpoints': [],
    'quick_calibrate': True,
    'cal_mtx' : None,   # camera calibration matrix
    'cal_dist': None,     # camera distortion coefficients
    'sobel_min_thresh' : 30,
    'sobel_max_thresh' : 100,
    'sobel_kernel_size' : 3,
    'sobel_out_depth' : cv2.CV_64F
}


#saver = iS.ImgSaver()
saver = None
vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)
fname_list = glob.glob("camera_cal/*.jpg")
if gpd['quick_calibrate']:
    fname_list = [fname_list[0]]
    

gpd['cal_mtx'] , gpd['cal_dist'] = ut.calibrate_camera(None, fname_list,
                                                       gpd['chessboard_nx'], gpd['chessboard_ny'],
                                                       gpd['objpoints'], gpd['imgpoints'])

vwr.show()
