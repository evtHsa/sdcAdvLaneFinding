#!/usr/bin/env python3

import pipe
import calibrate as cal
import util as ut
import ImgSaver as imgsvr
import ImgViewer as imgvwr
import pdb

#gViewer = imgvwr.ImgViewer()
gViewer = imgvwr.ImgViewer(w=4, h=4, rows=2, cols=2, title="demo")

f1 = 'camera_cal/calibration1.jpg'
f16 = 'camera_cal/calibration16.jpg'
push_debug = False

img1 = ir.read(f1)
img16 = ir.read(f16)

for i in range(1, 10):
    if i % 2 != 0:
        img = img1
        fname = "f1" + "_" + str(i)
    else:
        img = img16
        fname = "f16" + "_" + str(i)
    gViewer.push(img, fname)

gViewer.show(clear=True)
gViewer.show_immed(img1, "booger", None)
gViewer.show()


