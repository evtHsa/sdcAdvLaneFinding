import pdb
import ImgViewer as iv
import ImgUtil as iu
import cv2
import matplotlib.image as mpimg
import numpy as np
import glob
import os
import hashlib

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
        print("\n==========\n" +msg + "\n==========\n")
        pdb.set_trace()

def calibrate_camera(vwr, nx, ny, objpoints, imgpoints):
        # inputs:
        #         vwr: for showing intermediate images, may be None
        #         nx: number of corners in x dim of chessboard
        #         ny: number of corners in y dim of chessboard
        #
        # outputs:
        #         camera matrix
        #         distortion coefficients
        # see:
        #  CV =https://docs.opencv.org/2.4.1/modules/calib3d/doc
        #  CV/camera_calibration_and_3d_reconstruction.html#calibratecamera        

        objp = np.zeros((nx*ny,3), np.float32)
        objp[:,:2] = np.mgrid[0:nx,0:ny].T.reshape(-1, 2)
        
        for fname in glob.glob("camera_cal/*.jpg"):
                tmp = iu.img_read(fname, None)
                orig = np.copy(tmp)
                # they're not all 720x1280
                #print("shape(%s) = %s" % (fname, tmp.shape))
                tmp = iu.img_rgb2gray(tmp, vwr)
                
                ret, corners = cv2.findChessboardCorners(tmp, (nx, ny), None)
                if ret:
                        objpoints.append(objp)
                        imgpoints.append(corners)
                        iu.img_drawChessboardCorners(orig, nx,ny, corners, ret, vwr)
                else:
                        print("failed to find corners: %s" % fname)
                        iv._push(vwr, orig, "**NO CORNERS**")
                        
        # ret is the RMS reprojection error. usually between 0.1 & 1.0
        # per https://docs.opencv.org/3.3.1/d9/d0c/group__calib3d.html
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                           tmp.shape[::-1],None,None)
        iv._show(vwr, clear=True)
        return mtx, dist

def hash_ndarray(nda, title):
        s = nda.tostring()
        hash = hashlib.md5(s).hexdigest()
        return hash

def frange(lo, hi, nsteps):
    return [lo + (hi - lo) * float(step)/(nsteps - 1) for step in range(nsteps)]
        
def paired_frange(lo_start, lo_end, lo_steps, hi_start, hi_end, hi_steps):
    return [(x, y)
            for x in frange(lo_start, lo_end, lo_steps)
            for y in frange(hi_start, hi_end, hi_steps)
            if x < y]

    
