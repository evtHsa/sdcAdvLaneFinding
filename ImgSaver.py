import datetime as dt
import os
import matplotlib.image as mpimg
import os.path
import util as ut
import ImgUtil as iu
import cv2

class ImgSaver:
    # abstracts saving a bunch of files in a timestamp directory
    def __init__(self, d="test_out/"):
        d = d + dt.datetime.now().strftime("%a_%m%d%y_%H%M%S") + "/"
        self.outdir = d
        os.mkdir(d)

    def save(self, img, msg=""):
        assert(type(img) is iu.Image)
        img_data = img.img_data
        if img.type == 'bgr':
            img_data = cv2.cvtColor(img.img_data, cv2.COLOR_BGR2RGB)
        outf = self.outdir + os.path.basename(img.title) + "_" + msg + ".png"
        mpimg.imsave(outf, img_data, cmap=img.cmap)

