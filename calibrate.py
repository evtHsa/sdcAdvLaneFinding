#!/usr/bin/env python3

import ImRead as ir
import glob
import os
import matplotlib.pyplot as plt
import cv2


# code heavly borrowed from
#        + lesson 5: Camera Calibration: modules 10-12
#        + https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html
#        + https://docs.opencv.org/2.4.1/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#calibratecamera
#        +

def calibrate_camera(viewer):
    i = 0
    for fname in glob.glob("camera_cal/*.jpg"):
        basename = os.path.basename(fname)

        img = ir.read(fname)
        viewer.show_immed(img, "initial: " + fname)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        viewer.show_immed(gray, "gray: " + fname, cmap='Greys_r')
    print("FIXME:thats all folx")


    
