#
# this module may not need to continue existing. it was originally created to experiment
# between mpimg & cv2 variants of imread
#

import matplotlib.image as mpimg

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

@static_var("ctr", 0)

def read(path):
    read.ctr += 1
    img = mpimg.imread(path)
    #print("ImRead.read(%s): ctr = %d" % (path, read.ctr))
    return img
