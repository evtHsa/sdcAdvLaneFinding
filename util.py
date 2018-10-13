import pdb
import util as ut
import ImgViewer as iv
import ImgUtil as iu
import cv2
import matplotlib.image as mpimg
import numpy as np
import os
import hashlib
import glob

def ohBother(img):
        plt.figure()
        plt.imshow(img)
        plt.show()
        
def ohBother_g(img):
        plt.figure()
        plt.imshow(img, cmap='Greys_r')
        plt.show()  

def existsKey(dict, key):
        try:
                val = dict[key]
        except KeyError:
                return False
        return True


def safeGetDictVal(dict, key):
        if existsKey(dict, key):
                return dict[key]
        else:
                return None

def brk(msg=""):
        print("\n==========\n" +msg + "\n==========\n")
        pdb.set_trace()

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

    
one_shot_dict = { 'stooge' : 'curly'}

def oneShotMsg(msg):
        if not existsKey(one_shot_dict, msg):
                print(msg)
        one_shot_dict[msg] = msg

def init_obj_points(nx, ny):
    # derived from https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials \
    # /py_calib3d/py_calibration/py_calibration.html
    #
    # expanded a little from original terse version for my understanding

    ret  = np.zeros((ny*nx,3), np.float32)
    grid  = np.mgrid[0:nx, 0:ny]
    # grid shape is (2, nx, ny)
    # 0 plane has row vectors of identical components from 1 to nx
    # 1 plane has col vectors of identical components from 1 to nx
    # ex: if  nx = 2 and ny = 3
    #[[[0, 0, 0],
    #  [1, 1, 1]],
    #                            2nd row
    # [[0, 1, 2],
    #  [0, 1, 2]]])
    grid = grid.T
    # after the transpose we have ny  x nx x 2
    # almost have the nx * ny pairs we want
    grid = grid.reshape(-1, 2)
    # now we h avegrid = [[0, 0], [1, 0], [0, 1], [1, 1], [0, 2], [1, 2]]
    ret[:,:2] = grid
    # finally we end up with
    # [[0., 0, 0.], ...,
    # [1.,  0., 0.],
    # [0.,  1., 0.],
    # [1.,   1., 0.]
    # [0.,  2., 0.],
    # [1.,   2., 0.]
    return ret

def get_fnames(dir, pattern, max=0):
    # if max != 0, return up to max filenames, else all of them
    fnames = glob.glob(dir + pattern)
    if max:
        print("WARNING: only using %d files from %s" % (max, dir))
        fnames = fnames[0:max]
    return fnames
    
def cb_corners(parm_dict, cache_dict, max_files=0, verbose=False, vwr=None):
    # derived from same source as init_obj_points()
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    nx, ny = parm_dict['chessboard_nx'],  parm_dict['chessboard_ny']
    objp  = init_obj_points(nx, ny) # object points in 3 space

    obj_points = []
    img_points = [] # point in 2 space
    
    for fname in get_fnames("camera_cal/", "calibration*.jpg"):

        img_obj = iu.imRead(fname, reader='cv2', vwr=vwr)
        if verbose:
            print("cb_corners: fname = %s(%d, %d)" % (fname,
                                                      img_obj.shape()[0], img_obj.shape()[1]))
        gray = iu.cv2CvtColor(img_obj, cv2.COLOR_BGR2GRAY, vwr)
        
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray.img_data, (nx,ny), None)
        
        # If found, add object points, image points
        if ret == True:
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(gray.img_data,corners,(11,11),(-1,-1),criteria)
            img_points.append(corners2)
            
            # Draw and display the corners
            cv2.drawChessboardCorners(img_obj.img_data, (nx,ny), corners2, ret)
            iv._push(vwr, img_obj)
        else:
            print("findChessboardCorners(%s) failed" % fname)

    iv._show(vwr, clear=True)
    cache_dict['obj_points'] = obj_points
    cache_dict['img_points'] = img_points
              
