#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pipe
import calibrate as cal
import util as ut

gViewer = ut.ImgViewer(4,4)

def stage_fn_stub(img):
    print("boy howdy")
    return img

def stage_fn_img_read(path):
     img = mpimg.imread(path)
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
#demo_pipeline_2.exec(mpimg.imread('test_images/test1.jpg'))
#demo_pipeline_3.exec('camera_cal/calibration1.jpg')
#gViewer.push(mpimg.imread('camera_cal/calibration1.jpg'), title = 'curly')
#gViewer.push(mpimg.imread('camera_cal/calibration1.jpg'), title = 'moe')
#gViewer.push(mpimg.imread('camera_cal/calibration1.jpg'), title = '1: sleepy')
#gViewer.push(mpimg.imread('camera_cal/calibration1.jpg'), title = '2: sneezy')
#gViewer.push(mpimg.imread('camera_cal/calibration1.jpg'), title = '3: doc')
#gViewer.push(mpimg.imread('camera_cal/calibration1.jpg'), title = '4: dopey')
#gViewer.push(mpimg.imread('camera_cal/calibration1.jpg'), title = '5: bashful')
#gViewer.push(mpimg.imread('camera_cal/calibration1.jpg'), title = '6: grumpy')
#gViewer.push(mpimg.imread('camera_cal/calibration1.jpg'), title = '7: happy')
#
img = mpimg.imread('camera_cal/calibration1.jpg')
print("FIXME_1: shape = " + str(img.shape))
#img = mpimg.imread('camera_cal/calibration1.jpg')
#gViewer.push(img)
##

#gViewer.show()
cal.calibrate_camera(gViewer)
