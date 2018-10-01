#!/usr/bin/env python3

import pipe
import calibrate as cal
import util as ut
import ImgSaver as imgsvr
import ImgViewer as imgvwr
import ImRead as ir
import pdb

gViewer = imgvwr.ImgViewer(10, 6,"bummer", rows = 2, cols = 2)

f1 = 'camera_cal/calibration1.jpg'
f16 = 'camera_cal/calibration16.jpg'

img1 = ir.read(f1)
img16 = ir.read(f16)

for i in range(1, 8):
    gViewer.push(img1, f1 + "_" + str(i))
    gViewer.push(img16, f16 + "_" + str(i))

gViewer.show()
