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
import camera
import parm_dict as pd
import ImgSaver as iS

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

def get_fnames(dir, pattern, max=0):
    # if max != 0, return up to max filenames, else all of them
    fnames = glob.glob(dir + pattern)
    if max:
        print("WARNING: only using %d files from %s" % (max, dir))
        fnames = fnames[0:max]
    return fnames
    
              
def infrastructure_setup(viewer, saver, title):
     # setup the saver and viewer keys in cache_diict
     # returns: parm_dict, cache_dict
     cd   = pd.cache_dict
     pd_ = pd.parm_dict

     cd['viewer'] = None
     cd['saver'] = None
     if saver:
          cd['saver'] = iS.ImgSaver()
     if viewer:
          cd['viewer'] = iv.ImgViewer(w=pd_['viewer_width'], h=pd_['viewer_height'],
                                      rows=pd_['viewer_rows'], cols=pd_['viewer_cols'],
                                      title=title, svr=cd['saver'])
     return cd, pd_

def app_init(viewer=False, saver=False, title=""):
     # on return these keys will be set in cache_dict
     #        viewer, saver, mtx, dist, M_lookdown, M_lookdown_inv
     # returns: parm_dict, cache_dict
     cache_dict, parm_dict = infrastructure_setup(viewer, saver, title)
     camera.camera_setup(cache_dict = cache_dict, parm_dict = parm_dict)
     return (cache_dict, parm_dict)

def _assert(cond):
        if not cond:
                really_assert = True
                print("assertion failed")
                pdb.set_trace()
                if really_assert:
                        assert(False)
