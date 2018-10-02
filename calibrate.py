#!/usr/bin/env python3

import ImRead as ir
import glob
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
import ImgViewer as vwr


# code heavly borrowed from
#        + lesson 5: Camera Calibration: modules 10-12
#        + https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html
#        + https://docs.opencv.org/2.4.1/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#calibratecamera
#        +

def calibrate_camera(viewer, nx, ny):
    # inputs:
    #         viewer: for showing intermediate images, may be None
    #         nx: number of corners in x dim of chessboard
    #         ny: number of corners in y dim of chessboard
    #
    # outputs:
    #         camera matrix
    #         distortion coefficients
    # see:
    #  CV =https://docs.opencv.org/2.4.1/modules/calib3d/doc
    #  CV/camera_calibration_and_3d_reconstruction.html#calibratecamera        

    objpoints = []
    imgpoints = []
    objp = np.zeros((nx*ny,3), np.float32)
    objp[:,:2] = np.mgrid[0:nx,0:ny].T.reshape(-1, 2)

    for fname in glob.glob("camera_cal/*.jpg"):
        basename = os.path.basename(fname)

        img = ir.read(fname)
        vwr._view(viewer, img, "initial: " + fname)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        vwr._view(viewer, gray, "gray: " + fname, cmap='Greys_r')
        ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                           gray.shape[::-1],None,None)

    #print("mtx = " + str(mtx))
    #print("objp.shape = %s" % str(objp.shape))
    return mtx, dist



    
