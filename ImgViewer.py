import numpy as np
import matplotlib.pyplot as plt
import ImRead as ir

class ImgViewer:
    # for debug - usage demo
    #    
    #    binary_warped = ir.read('test_images/test1.jpg')
    #    imgViewer = ImgViewer(30, 30)
    #    for i in range(1,10):
    #        imgViewer.push(binary_warped, "some_title' + str(i))

    #    
    def __init__(self, w, h, title, rows=1, cols=1):
        self.img_parms_list = []
        self.w = w
        self.h = h
        self.title = title
        self.fig = plt.figure(figsize=(self.w, self.h), num=self.title)
        self.rows = rows
        self.ax_list = []
        self.cols = cols

        for i in range(rows * cols):
            print("FIXME: i = " + str(i))
            ax = self.fig.add_subplot(rows, cols , i + 1)
            self.ax_list.append(ax)
            ax.set_xticks(())
            ax.set_yticks(())

    def push(self, img_ref, title=""):
        self.img_parms_list.append({'img_ref' : np.copy(img_ref), 'title' : title})
        l = len(self.img_parms_list)

    def show_1_grid(self, start):
        n_imgs = len(self.img_parms_list)
        if (start >= n_imgs):
            return
        print("FIXME:beware old content on last gridfull")
        print("FIXME, FIXME, FIXME: call show_1_grid(%d)" % start)
        grid_size = self.rows * self.cols
            
        import pdb
        pdb.set_trace()
        for i in range(grid_size):
            ix = start
            
            ax = self.ax_list[i]
            img_ref = self.img_parms_list[i]['img_ref']
            img_title = self.img_parms_list[i]['title']
            ax.set_title(img_title)
            plt.imshow(img_ref, cmap='Greys_r')
        
        plt.show()

        def clear(self):
            img_parms_list
            print("FIXME: may want to clear frame here too")

    def show(self, clear = False):
        print("FIXME: n = %d" % (len(self.img_parms_list)))
        plt.xticks(())
        plt.yticks(())

        n_imgs = len(self.img_parms_list)
        grid_size = self.rows * self.cols
        for i in range(0, n_imgs, grid_size):
            self.show_1_grid(i)
        if clear:
            self.clear()


    def dump(self):
        if  len(self.img_parms_list) < 1:
            raise Exception("nothing to show")
        for _img_parms in self.img_parms_list:
            img_ref = _img_parms['img_ref']
            plt.figure()
            plt.imshow(img_ref, cmap='Greys_r')
            plt.show()
            

    def flush(self):
        self.img_parms_list = []

