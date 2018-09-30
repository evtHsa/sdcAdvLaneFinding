#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pipe

def stage_fn_stub(img):
    print("boy howdy")
    return img

def stage_fn_img_read(path):
     img = mpimg.imread(path)
     return img

demo_pipeline = pipe.Pipe(
    [pipe.PipeStage(stage_fn_img_read,
                    {'name' : 'imgread', 'debug_level' : 2}),
     pipe.PipeStage(stage_fn_stub,
                    {'name' : 'stub1', 'debug_level' : 2}),
     pipe.PipeStage(stage_fn_stub,
                    {'name' : 'stub2', 'debug_level' : 2})
     ],
    {'debug_level ': 3})

demo_pipeline.exec('test_images/test1.jpg')
