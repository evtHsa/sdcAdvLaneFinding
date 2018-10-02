import numpy as np
import matplotlib.pyplot as plt
import ImRead as ir
import pdb

class ImgViewer:
    # for debug - usage demo
    #    
    #    binary_warped = ir.read('test_images/test1.jpg')
    #    imgViewer = ImgViewer(30, 30)
    #    for i in range(1,10):
    #        imgViewer.push(binary_warped, "some_title' + str(i))

    #    
    def __init__(self, w, h, title, rows=1, cols=1):
        raise Exception("not sure why this show updates of plot but, for now, it is useless")
        self.img_parms_list = []
        self.w = w
        self.h = h
        self.title = title
        self.fig = plt.figure(figsize=(self.w, self.h), num=self.title)
        self.rows = rows
#      self.ax_list = []
        self.cols = cols

#        for i in range(rows * cols):
#            ax = self.fig.add_subplot(rows, cols , i + 1)
#            self.ax_list.append(ax)
#            ax.set_xticks(())
#            ax.set_yticks(())

    def __init__(self):
        pass #doesn't do much, does it?

    def clear_sub_plots(self):
        #return;
        for i in range(rows * cols):
            self.ax_list[i].cla()
            
    def push(self, img_ref, title="", debug=False):
        L = self.img_parms_list
        L.append({'img_ref' : np.copy(img_ref), 'title' : title})
        print("push: len = %d, title = %s"  %  (len(L), title))

    def show_1_grid(self, start):
        L = self.img_parms_list
        n_imgs = len(L)
        print("FIXME, FIXME, FIXME: show_1_grid(%d)" % start)
        if (start >= n_imgs):
            return
        print("FIXME:beware old content on last gridfull")
        grid_size = self.rows * self.cols
            
        #pdb.set_trace()
        for i in range(grid_size):
            ix = start + i
            if (ix >= n_imgs):
                print("FIXME: out of images")
                break
            ax = self.fig.add_subplot(self.rows, self.cols , i + 1)
            ax.set_xticks(())
            ax.set_yticks(())
            img_ref = L[ix]['img_ref']
            img_title = L[ix]['title']
            print("title = " + img_title)
            ax.set_title(img_title)
            ax.imshow(img_ref, cmap='Greys_r')
        
        plt.show(block=True)
        pdb.set_trace()

        def clear(self):
            img_parms_list 
            print("FIXME: may want to clear frame here too")

    def show(self, clear = False):
        L = self.img_parms_list
        print("FIXME: n = %d" % (len(L)))

        n_imgs = len(L)
        grid_size = self.rows * self.cols
        for i in range(0, n_imgs, grid_size):
            self.show_1_grid(i)
        pdb.set_trace()

    def dump(self):
        L = self.img_parms_list
        if  len(L) < 1:
            raise Exception("nothing to show")
        for _img_parms in L:
            img_ref = _img_parms['img_ref']
            self.fig.figure()
            self.fig.imshow(img_ref, cmap='Greys_r')
            self.fig.show()
            

    def flush(self):
        self.img_parms_list = []

    def show_immed(self, img, title="", cmap=None):
        plt.figure()
        plt.title(title)
        if cmap:
            plt.imshow(img, cmap=cmap)
        else:
            plt.imshow(img)
        plt.show()    


