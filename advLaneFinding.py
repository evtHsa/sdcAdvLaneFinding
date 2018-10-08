#!/usr/bin/env python3


import demo
import  cv2
import ImgViewer as iv
import ImgSaver as iS

# FIXME: may want to tweak some of thse parms
# gpd -> global parm dict
gpd ={ 
    'chessboard_nx' : 9,
    'chessboard_ny' : 6,
    'objpoints' : [],
    'imgpoints': [],
    'cal_mtx' : None,
    'cal_dist': None,
    'sobel_min_thresh' : 30,
    'sobel_max_thresh' : 100,
    'sobel_kernel_size' : 3,
    'sobel_out_depth' : cv2.CV_64F
}


#saver = iS.ImgSaver()
saver = None
vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)


#lane_finding_take_1('test_images/signs_vehicles_xygrad.png')

demo.doit_6_12('test_images/bridge_shadow.jpg', vwr=vwr)

vwr.show()
