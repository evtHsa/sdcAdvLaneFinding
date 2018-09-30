#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import util as ut
import glob

# code heavly borrowed from
#        + lesson 5: Camera Calibration: modules 10-12
#        + https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html
#        + https://docs.opencv.org/2.4.1/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#calibratecamera
#        +

def calibrate_camera():
    for fname in glob.glob("camera_cal/*.jpg"):
        print("FIXME: fname = " + fname)

    
