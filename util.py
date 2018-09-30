#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import datetime as dt
import os
import os.path

class ImgViewer:
    # for debug - usage demo
    #    
    #    binary_warped = mpimg.imread('test_images/test1.jpg')
    #    imgViewer = ImgViewer(30, 30)
    #    for i in range(1,10):
    #        imgViewer.push(binary_warped, "some_title' + str(i))

    #    
    def __init__(self, w, h):
        self.img_parms_list = []
        self.w = w
        self.h = h

    def push(self, img_ref, title="larry"):
        self.img_parms_list.append({'img_ref' : img_ref, 'title' : title})

    def show(self,  cols = 2):
        if  len(self.img_parms_list) < 1:
            raise Exception("nothing to show")
        rows = int(np.ceil(len(self.img_parms_list) / cols))
        #print("FIXME: rows = %d, cols = %d" % (rows, cols))
        
        fig = plt.figure(figsize=(self.w, self.h))
        for i , _img_parms in zip(range(1, len(self.img_parms_list) + 1), self.img_parms_list):
            img_ref = _img_parms['img_ref']
            ax = fig.add_subplot(rows, cols , i)
            ax.set_title(_img_parms['title'])
            plt.imshow(img_ref, cmap='Greys_r')
        plt.show()

    def flush(self):
        self.img_parms_list = []

class ImgSaver:
    # abstracts saving a bunch of files in a timestamp directory
    def __init__(self):
        d = "test_out/"
        d = d + dt.datetime.now().strftime("%a_%m%d%y_%H%M%S") + "/"
        self.outdir = d
        os.mkdir(d)

    def save(self, img, img_name, cmap='Greys_r', msg=""):
        outf = self.outdir + img_name + "_" + msg + ".png"
        if cmap:
            mpimg.imsave(outf, img, cmap=cmap)
        else:
            mpimg.imsave( outf, img)

def ohBother(img):
        plt.figure()
        plt.imshow(img)
        plt.show()
        
def ohBother_g(img):
        plt.figure()
        plt.imshow(img, cmap='Greys_r')
        plt.show()  
