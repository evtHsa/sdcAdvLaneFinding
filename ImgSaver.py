import datetime as dt
import os
import matplotlib.image as mpimg
import os.path

class ImgSaver:
    # abstracts saving a bunch of files in a timestamp directory
    def __init__(self, d="test_out/"):
        raise Exception("FIXME: this is broken")
        d = d + dt.datetime.now().strftime("%a_%m%d%y_%H%M%S") + "/"
        self.outdir = d
        os.mkdir(d)

    def save(self, img_obj, msg=""):
        outf = self.outdir + os.path.basename(imb_obj.title) + "_" + msg + ".png"
        mpimg.imsave(outf, img, cmap=cmapimg_obj.cmap)

