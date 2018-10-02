#!/usr/bin/env python3

import pipe
import calibrate as cal
import util as ut
import ImgSaver as imgsvr
import ImgViewer as imgvwr
import ImRead as ir
import pdb

gViewer = imgvwr.ImgViewer()

f1 = 'camera_cal/calibration1.jpg'
f16 = 'camera_cal/calibration16.jpg'
push_debug = False

img1 = ir.read(f1)
img16 = ir.read(f16)

for i in range(1, 8):
    gViewer.show_immed(img1, f1 + "_" + str(i))
    gViewer.show_immed(img16, f16 + "_" + str(i))


