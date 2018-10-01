import ImgViewer as imgvwr

class PipeStage:

    def __init__(self, fn, hyper_parms):
        self.fn = fn
        self.hyper_parms = hyper_parms

    def exec(self, img, pipe_parms):
        return  self.fn(img)


class Pipe:

    def __init__(self, stage_list, parm_dict, viewer=None):
        self.stage_list = stage_list
        self.pipe_parm_dict = parm_dict
        try:
            self.imgViewer = parm_dict['viewer']
        except:
            self.imgViewer = imgvwr.ImgViewer(4,4)

    def exec(self, img):
        # unenforced convention img can also be a path for pipes where the
        # first stage reads an image from the path
        tmp = img
        for stage in self.stage_list:
            stage_name = stage.hyper_parms['name']
            print("stage: %s" % stage_name)
            tmp = stage.exec(tmp, None)

            none_type = type(None) # FIXME
            if type(tmp) != none_type: # stages must return img or None
                self.imgViewer.push(tmp, stage_name)
        self.imgViewer.show()
            
