#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

class PipeStage:

    def __init__(self, fn, hyper_parms):
        self.fn = fn
        self.hyper_parms = hyper_parms

    def exec(self, img, pipe_parms):
        self.fn(img)


class Pipe:

    def __init__(self, stage_list, pipe_parm_dict):
        self.stage_list = stage_list
        self.pipe_parm_dict = pipe_parm_dict

    def exec(self, img):
        tmp = img
        for stage in self.stage_list:
            tmp = stage.exec(tmp, None)
            
