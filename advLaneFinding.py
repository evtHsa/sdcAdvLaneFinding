#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import util as ut
import pipe

def stage_fn_stub(img):
    print("boy howdy")

# TODO: define an img read from disk stage
# TODO: define a img display stage
# TODO: define imgViewer in pipe::exec

pipeline = pipe.Pipe(
    [pipe.PipeStage(stage_fn_stub,
                    {'name' : 'stub', 'debug_level' : 2}),
     pipe.PipeStage(stage_fn_stub,
                    {'name' : 'stub2', 'debug_level' : 2})
     ],
    {'debug_level ': 3})

pipeline.exec(None)
