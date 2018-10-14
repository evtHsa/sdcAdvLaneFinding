#

import cv2
import util as ut
import ImgUtil as iu

def calibrateCamera(parms=None, cache = None, vwr = None):
     ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(cache['obj_points'],
                                                        cache['img_points'],
                                                        parms['camera_resolution'],
                                                        None, None)
     cache['mtx'] = mtx
     cache['dist'] = dist

def camera_setup(cache_dict=None, parm_dict=None):
     vwr = cache_dict['viewer']
     iu.cb_corners(parm_dict, cache_dict, max_files=0, verbose=False,
                   vwr=None) #(obj,img)_points in cache
     calibrateCamera(parms=parm_dict, cache = cache_dict, vwr=vwr)
     # now have mtx and dist in cache
     
     iu.getLookDownXform(cache_dict) # cache['M_lookdown[_inv]']

