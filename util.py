import pdb


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
