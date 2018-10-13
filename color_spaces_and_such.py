#!/usr/bin/env python3

import util as ut
import ImgViewer as iv
import ImgUtil as iu
import parm_dict as pd

parm_dict = pd.parm_dict
cache_dict = pd.cache_dict

#saver = iS.ImgSaver()
saver = None

vwr = iv.ImgViewer(w=5, h=5, rows=2, cols=2, title="lane_finding_take1", svr=saver)

ut.cb_corners(parm_dict, cache_dict, max_files=0, verbose=False,
              vwr=None) #(obj,img)_points in cache
iu.calibrateCamera(parms=parm_dict, cache = cache_dict, vwr=vwr)
# now have mtx and dist in cache
iu.getLookDownXform(cache_dict) # cache['M_lookdown[_inv]']
ut.brk("wtf andy?")


