#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

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

    def show(self):
        if  len(self.img_parms_list) < 1:
            raise Exception("nothing to show")
        rows = int(np.ceil(np.sqrt(len(self.img_parms_list))))
        cols = rows
        print("rows = %d, cols = %d" % (rows, cols))
        
        fig = plt.figure(figsize=(self.w, self.h))
        for i , img_parms in zip(range(1, len(self.img_parms_list) + 1), self.img_parms_list):
            img_ref = img_parms['img_ref']
            ax = fig.add_subplot(rows, cols , i)
            ax.set_title(img_parms['title'])
            plt.imshow(img_ref)
        plt.show()

