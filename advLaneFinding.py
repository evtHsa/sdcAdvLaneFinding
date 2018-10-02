#!/usr/bin/env python3

import pipe
import calibrate as cal
import util as ut
import ImgSaver as imgsvr
import ImgViewer as imgvwr
import ImRead as ir

#gViewer = imgvwr.ImgViewer(4,4)
gViewer = imgvwr.ImgViewer()

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
#demo_pipeline_3.exec('camera_cal/calibration1.jpg')
#gViewer.push(ir.read('camera_cal/calibration1.jpg'), title = 'curly')
#gViewer.push(ir.read('camera_cal/calibration1.jpg'), title = 'moe')
#gViewer.push(ir.read('camera_cal/calibration1.jpg'), title = '1: sleepy')
#gViewer.push(ir.read('camera_cal/calibration1.jpg'), title = '2: sneezy')
#gViewer.push(ir.read('camera_cal/calibration1.jpg'), title = '3: doc')
#gViewer.push(ir.read('camera_cal/calibration1.jpg'), title = '4: dopey')
#gViewer.push(ir.read('camera_cal/calibration1.jpg'), title = '5: bashful')
#gViewer.push(ir.read('camera_cal/calibration1.jpg'), title = '6: grumpy')
#gViewer.push(ir.read('camera_cal/calibration1.jpg'), title = '7: happy')
#

#img = ir.read('camera_cal/calibration16.jpg')
#gViewer.push(img, "frm main")
#gViewer.show()

chess_b_nx = 9 # per assignment overview
chess_b_ny = 6 # per assignment overview
cal.calibrate_camera(gViewer, chess_b_nx, chess_b_ny)
