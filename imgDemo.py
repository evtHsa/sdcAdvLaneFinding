#!/usr/bin/env python3

import pipe
import calibrate as cal
import util as ut
import ImgSaver as imgsvr
import ImgViewer as imgvwr
import ImRead as ir

gViewer = imgvwr.ImgViewer(8,4,"bummer")

fname = 'camera_cal/calibration1.jpg'

img = ir.read(fname)
for i in range(1,4):
    gViewer.push(img, fname)
gViewer.show()


