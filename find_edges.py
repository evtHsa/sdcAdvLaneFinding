#!/usr/bin/env python3

import util as ut

cache_dict, parm_dict = ut.app_init(viewer=True, saver=False, title="whatever")
vwr = cache_dict['viewer']

tmp = iu.img_read("test_images/straight_lines2.jpg", vwr)
ut.brk("as it stands, this test is pretty useless")

vwr.show()
