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
        #@Undistort the image using cv2.undistort() with mtx and dist
        #@Convert to grayscale
        # Find the chessboard corners
        # Draw corners
        # Define 4 source points (the outer 4 corners detected in the chessboard pattern)
        # Define 4 destination points (must be listed in the same order as src points!)
        # Use cv2.getPerspectiveTransform() to get M, the transform matrix
        # use cv2.warpPerspective() to apply M and warp your image to a top-down view
        pipe.PipeStage(pipe.stage_fn_img_read,
                       {'name' : 'imgread', 'debug_level' : 2}),
        pipe.PipeStage(pipe.stage_fn_undistort,
                       {'name' : 'undistort', 'debug_level' : 2, 'cmap' : 'Greys_r'}),
        pipe.PipeStage(pipe.stage_fn_rgb2gray,
                       {'name' : 'undistort', 'debug_level' : 2, 'cmap' : 'Greys_r'})
    ],
    {'debug_level ': 3, 'viewer' : gViewer})

chess_b_nx = 9 # per assignment overview
chess_b_ny = 6 # per assignment overview
ppd = demo_pipeline_3.get_parm_dict()
ppd['cal_mtx'] , ppd['cal_dist'] = cal_mtx, cal_dist = cal.calibrate_camera(None,
                                                                            chess_b_nx, chess_b_ny)

demo_pipeline_3.exec('test_images/test1.jpg')
print("FIXME: need to review get perspective transform and my code in the excercise")
print("FIXME:specifically how I chose the poiints")

#snippets from notes(srch ntbk for goober_pease
#Compute the perspective transform, M, given source and destination points:
#M = cv2.getPerspectiveTransform(src, dst)


#Compute the inverse perspective transform:
#Minv = cv2.getPerspectiveTransform(dst, src)


#Warp an image using the perspective transform, M:
#warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)


#Note: When you apply a perspective transform, choosing four source points manually, as we did in this video, is often not the best option. There are many other ways to select source points. For example, many perspective transform algorithms will programmatically detect four source points in an image based on edge or corner detection and analyzing attributes like color and surrounding pixels.
