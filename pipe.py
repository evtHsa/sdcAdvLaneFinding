import ImgViewer as imgvwr
import ImRead as ir
import util as ut
import cv2

class PipeStage:

    def __init__(self, fn, hyper_parms):
        self.fn = fn
        self.hyper_parms = hyper_parms

    def exec(self, img, pipe_parms):
        return  self.fn(img, pipe_parms)


class Pipe:

    def __init__(self, stage_list, parm_dict, viewer=None):
        self.stage_list = stage_list
        self.pipe_parm_dict = parm_dict
        self.imgViewer = ut.safeGetDictVal(parm_dict, 'viewer')

    def get_parm_dict(self):
        return self.pipe_parm_dict

    def exec(self, img):
        # unenforced convention img can also be a path for pipes where the
        # first stage reads an image from the path
        tmp = img
        for stage in self.stage_list:
            stage_name = stage.hyper_parms['name']
            print("stage: %s" % stage_name)
            tmp = stage.exec(tmp, self.pipe_parm_dict)

            none_type = type(None) # FIXME
            if type(tmp) != none_type: # stages must return img or None
                cmap = ut.safeGetDictVal(stage.hyper_parms, 'cmap')
                self.imgViewer.push(tmp, stage_name, cmap=cmap)
        self.imgViewer.show()
            
def stage_fn_stub(img, ppd):
    print("boy howdy")
    return img

def stage_fn_img_read(path, ppd):
     img = ir.read(path)
     return img

def stage_fn_rgb2gray(img, ppd):
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    return gray

def stage_fn_undistort(img, ppd):
    # ppd -> pipeline parm dict
    mtx = ppd['cal_mtx']
    dist = ppd['cal_dist']
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    return undist

demo_pipeline_1 = Pipe(
    [ 
        PipeStage(stage_fn_img_read,
                       {'name' : 'imgread', 'debug_level' : 2}),
        PipeStage(stage_fn_stub,
                       {'name' : 'stub1', 'debug_level' : 2}),
        PipeStage(stage_fn_stub,
                       {'name' : 'stub2', 'debug_level' : 2})
     ],
    {'debug_level ': 3})

demo_pipeline_2 = Pipe(
    [
        PipeStage(stage_fn_stub,
                       {'name' : 'stub1', 'debug_level' : 2}),
        PipeStage(stage_fn_stub,
                       {'name' : 'stub2', 'debug_level' : 2})
    ],
    {'debug_level ': 3})


#demo_pipeline_1.exec('test_images/test1.jpg')
#demo_pipeline_2.exec(ir.read('test_images/test1.jpg'))
