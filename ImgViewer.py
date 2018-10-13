import numpy as np
import matplotlib.pyplot as plt
import util as ut
import ImgUtil as iu
    
class ImgViewer:
    
    def __init__(self, w=4, h=4, rows=1, cols=1, title = "", svr=None):
        self.img_obj_list = []
        self.w = w
        self.h = h
        self.title = title
        self.rows = rows
        self.cols = cols
        self.svr = svr

    def push(self, img_obj,  debug=False):
        assert(type(img_obj) is iu.Image)

        self.img_obj_list.append(img_obj)

        debug =  True
        if (debug):
            img_obj.show()
    
        if self.svr:
            self.svr.save(img, title)

    def pop(self):
        return self.img_obj_list.pop()

    def flush(self):
        self.img_parms = []

    def show_1_grid(self, start):
        L = self.img_obj_list
        n_imgs = len(L)

        plt.figure(figsize=(self.w, self.h))
        for i in range(self.rows * self.cols):
            ix = start + i
            if ix >= n_imgs:
                break
            plt.subplot(self.rows, self.cols, i + 1)
            L[ix].plot(_plt=plt)
            plt.xticks([], [])
            plt.yticks([], [])
        plt.show()
        
    def show(self, clear=False):
        L = self.img_obj_list
        n_imgs = len(L)
        grid_size = self.rows * self.cols

        for i in range(0, n_imgs, grid_size):
            self.show_1_grid(i)
        if clear:
            self.flush()

    def show_immed(self, img, title="", cmap=None):
        plt.figure()
        plt.title(title)
        if cmap:
            plt.imshow(img, cmap=cmap)
        else:
            plt.imshow(img)
        plt.show()

def _view(vwr, img, title, cmap=None):
    # turn off viewing by passing None as viewer
    if vwr:
        vwr.show_immed(img, title, cmap)
    
def _push(vwr, img_obj):
    if vwr:
        vwr.push(img_obj)

def _flush(vwr):
    if vwr:
        vwr.flush()

def _pop(vwr):
    if vwr:
        vwr.pop()

def _show(vwr, clear=False):
    if vwr:
        vwr.show(clear)
