#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Load our image - this should be a new frame since last time!
binary_warped = mpimg.imread('test_images/test1.jpg')
#print("binary_warped = " + str(binary_warped))


class ImgViewer:
    def __init__(self):
        self.img_refs = []
        self.w = 10
        self.h = 10

    def push(self, img_ref):
        self.img_refs.append(img_ref)

    def show(self):
        if  len(self.img_refs) < 1:
            raise Exception("nothing to show")
        rows = np.sqrt(len(self.img_refs))
        cols = rows
        print("rows = %d, cols = %d" % (rows, cols))
        
        fig = plt.figure(figsize=(8,8))
        for i , img_ref in zip(range(1, len(self.img_refs) + 1), self.img_refs):
            fig.add_subplot(4,5, i)
            plt.imshow(img_ref)
        plt.show()


imgViewer = ImgViewer()
#for i in range(1,10):
#    imgViewer.push(binary_warped)

imgViewer.push(binary_warped)
imgViewer.show()
