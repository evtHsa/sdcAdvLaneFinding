#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import LaneUtils as lu

# our object model
# Lanes:  contain LaneBoundary(s) and attributes common to both boundaries
# LaneBoundary(s): contain attributes for a particular lane bounday
# Windows: are used to calculate lane boundaries

#cd is cache_dict, pd is parm_dict
cd, pd = ut.app_init(viewer=True, saver=True, title="whatever")
