#!/usr/bin/env python3

import pipe
import calibrate as cal
import util as ut
import ImgSaver as imgsvr
import ImgViewer as imgvwr
import pipe as pipe

gViewer = imgvwr.ImgViewer(w=4, h=4, rows=2, cols=2, title="advLaneFind")

demo_pipeline_3 = pipe.Pipe(
    [
        pipe.PipeStage(pipe.stage_fn_img_read,
                       {'name' : 'imgread', 'debug_level' : 2}),
        pipe.PipeStage(pipe.stage_fn_rgb2gray,
                       {'name' : 'rgb2gray', 'debug_level' : 2, 'cmap': 'Greys_r'}),
        pipe.PipeStage(pipe.stage_fn_undistort,
                       {'name' : 'undistort', 'debug_level' : 2, 'cmap': 'Greys_r'})
    ],
    {'debug_level ': 3, 'viewer' : gViewer})

chess_b_nx = 9 # per assignment overview
chess_b_ny = 6 # per assignment overview
ppd = demo_pipeline_3.get_parm_dict()
ppd['cal_mtx'] , ppd['cal_dist'] = cal_mtx, cal_dist = cal.calibrate_camera(None,
                                                                            chess_b_nx, chess_b_ny)

demo_pipeline_3.exec('camera_cal/calibration1.jpg')
ut.brk()

