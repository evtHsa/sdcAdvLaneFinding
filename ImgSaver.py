import datetime as dt
import os

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
