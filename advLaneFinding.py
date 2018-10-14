#!/usr/bin/env python3

import util as ut
import demo
import  cv2
import ImgSaver as iS
import ImgUtil as iu
import ImgViewer as iv

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']

tmp = iu.imRead("test_images/straight_lines2.jpg", reader='mpimg', vwr=vwr)

vwr.show()
