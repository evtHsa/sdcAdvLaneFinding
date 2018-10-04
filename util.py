import pdb
import ImgViewer as iv
import cv2
import matplotlib.image as mpimg

def ohBother(img):
        plt.figure()
        plt.imshow(img)
        plt.show()
        
def ohBother_g(img):
        plt.figure()
        plt.imshow(img, cmap='Greys_r')
        plt.show()  

def safeGetDictVal(dict, key):
        try:
                val = dict[key]
        except KeyError:
                val = None
        return val

def brk(msg=""):
        print(msg + "\n\n")
        pdb.set_trace()

def img_read(path, viewer=None):
     img = mpimg.imread(path)
     iv._push(viewer, img, "img_read: " + path)
     return img

def rgb2gray(img, viewer=None):
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        iv._push(viewer, gray, "gray: ", 'Greys_r')
        return gray
        
def img_undistort(img, mtx, dist, viewer=None):
        print("FIXME: None?????????????")
        undist = cv2.undistort(img, mtx, dist, None, mtx)
        iv._push(viewer, img, "undistort: ")
        return undist
