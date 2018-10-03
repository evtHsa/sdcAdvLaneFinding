#!/usr/bin/env python3

import pipe
import calibrate as cal
import util as ut
import ImgSaver as imgsvr
import ImgViewer as imgvwr
import ImRead as ir
import cv2
import pdb

gViewer = imgvwr.ImgViewer(w=4, h=4, rows=2, cols=2, title="advLaneFind")

def stage_fn_stub(img):
    print("boy howdy")
    return img

def stage_fn_img_read(path):
     img = ir.read(path)
     return img

def stage_fn_rgb2gray(img):
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    return gray

demo_pipeline_1 = pipe.Pipe(
    [ 
        pipe.PipeStage(stage_fn_img_read,
                       {'name' : 'imgread', 'debug_level' : 2}),
        pipe.PipeStage(stage_fn_stub,
                       {'name' : 'stub1', 'debug_level' : 2}),
        pipe.PipeStage(stage_fn_stub,
                       {'name' : 'stub2', 'debug_level' : 2})
     ],
    {'debug_level ': 3})

demo_pipeline_2 = pipe.Pipe(
    [
        pipe.PipeStage(stage_fn_stub,
                       {'name' : 'stub1', 'debug_level' : 2}),
        pipe.PipeStage(stage_fn_stub,
                       {'name' : 'stub2', 'debug_level' : 2})
    ],
    {'debug_level ': 3})

demo_pipeline_3 = pipe.Pipe(
    [
        pipe.PipeStage(stage_fn_img_read,
                       {'name' : 'imgread', 'debug_level' : 2}),
        pipe.PipeStage(stage_fn_rgb2gray,
                       {'name' : 'stub2', 'debug_level' : 2})
    ],
    {'debug_level ': 3, 'viewer' : gViewer})

#demo_pipeline_1.exec('test_images/test1.jpg')
#demo_pipeline_2.exec(ir.read('test_images/test1.jpg'))
#

#img = ir.read('camera_cal/calibration16.jpg')
#gViewer.push(img, "frm main")
#gViewer.show()

chess_b_nx = 9 # per assignment overview
chess_b_ny = 6 # per assignment overview
ppd = demo_pipeline_3.get_parm_dict()
ppd['cal_mtx'] , ppd['cal_dist'] = cal_mtx, cal_dist = cal.calibrate_camera(None,
                                                                            chess_b_nx, chess_b_ny)
raise Exception("add a stage to do undistort")
demo_pipeline_3.exec('camera_cal/calibration1.jpg')

