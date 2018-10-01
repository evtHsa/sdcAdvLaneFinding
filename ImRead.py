
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
    print("ImRead.read(%s): ctr = %d" % (path, read.ctr))
    #print(str(img))
    return img
