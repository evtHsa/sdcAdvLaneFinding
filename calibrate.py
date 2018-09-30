#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import util as ut
import glob
import os.path

# code heavly borrowed from
#        + lesson 5: Camera Calibration: modules 10-12
#        + https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html
#        + https://docs.opencv.org/2.4.1/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#calibratecamera
#        +

def calibrate_camera():
    saver = ut.ImgSaver()
    
    for fname in glob.glob("camera_cal/*.jpg"):
        basename = os.path.basename(fname)
        print("FIXME: fname = " + fname)
        img = mpimg.imread(fname)
        #saver.save(img, basename,  msg="init")
        ut.ohBother(img)
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        #saver.save(gray, basename,  msg="gray")
        ut.ohBother_g(img)
        break
    print("FIXME:thats all folx")


    
