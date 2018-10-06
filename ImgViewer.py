import numpy as np
import matplotlib.pyplot as plt

import pdb

class ImgViewer:
    # for debug - usage demo
    #    


    def __init__(self, w=4, h=4, rows=1, cols=1, title = "",):
        self.img_parms_list = []
        self.w = w
        self.h = h
        self.title = title
        self.rows = rows
        self.cols = cols

    def push(self, img_ref, title="", debug=False, cmap=None):
        L = self.img_parms_list
        L.append({'img_ref' : np.copy(img_ref), 'title' : title, 'cmap': cmap})
        print("push: len = %d, title = %s, cmap = %s"  %  (len(L), title, cmap))

    def flush(self):
        self.img_parms_list = []

    def show_1_grid(self, start):
        L = self.img_parms_list
        n_imgs = len(L)
        #print("\tFIXME:show_1_grid(%d)" % start)

        plt.figure(figsize=(self.w, self.h))
        for i in range(self.rows * self.cols):
            ix = start + i
            if ix >= n_imgs:
                break
            img_parms = L[ix]
            plt.subplot(self.rows, self.cols, i + 1)
            img_parms = L[ix]
            cmap = img_parms['cmap']
            if cmap:
                plt.imshow(img_parms['img_ref'], cmap=cmap)
            else:
                plt.imshow(img_parms['img_ref'])
            plt.xlabel(img_parms['title'])
            plt.xticks([], [])
            plt.yticks([], [])
        plt.show()
        
    def show(self, clear=False):
        #print("FIXME:show_2")
        L = self.img_parms_list
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
    
def _push(vwr, img, title, cmap=None):
    if vwr:
        vwr.push(img, title, cmap=cmap)
