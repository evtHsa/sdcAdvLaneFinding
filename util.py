import pdb
import ImgViewer as iv
import ImgUtil as iu
import cv2
import matplotlib.image as mpimg
import numpy as np
import glob
import os

def ohBother(img):
        plt.figure()
        plt.imshow(img)
        plt.show()
        
def ohBother_g(img):
        plt.figure()
        plt.imshow(img, cmap='Greys_r')
        plt.show()  

def safeGetDictVal(dict, key):
        try:
                val = dict[key]
        except KeyError:
                val = None
        return val

def brk(msg=""):
        print(msg + "\n\n")
        pdb.set_trace()

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
        tmp = iu.img_read(fname, None)
        tmp = iu.img_rgb2gray(tmp, None)

        ret, corners = cv2.findChessboardCorners(tmp, (nx, ny), None)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                           tmp.shape[::-1],None,None)

    #print("mtx = " + str(mtx))
    #print("objp.shape = %s" % str(objp.shape))
    return mtx, dist



    
