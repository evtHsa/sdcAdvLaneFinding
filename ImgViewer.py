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
    def __init__(self, w, h, title):
        self.img_parms_list = []
        self.w = w
        self.h = h
        self.title = title
        self.fig = plt.figure(figsize=(self.w, self.h), num=self.title)

    def push(self, img_ref, title="larry"):
        l = len(self.img_parms_list)
        if l > 4:
            print("FIXME:i am full")
            return
        
        self.img_parms_list.append({'img_ref' : np.copy(img_ref), 'title' : title})

    def show(self,  cols = 2):
        if  len(self.img_parms_list) < 1:
            raise Exception("nothing to show")
        rows = int(np.ceil(len(self.img_parms_list) / cols))
        #print("FIXME: rows = %d, cols = %d" % (rows, cols))
        
        for i , _img_parms in zip(range(1, len(self.img_parms_list) + 1), self.img_parms_list):
            img_ref = _img_parms['img_ref']
            ax = self.fig.add_subplot(rows, cols , i)
            ax.set_title(_img_parms['title'])
            plt.imshow(img_ref, cmap='Greys_r')
        plt.show()

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
