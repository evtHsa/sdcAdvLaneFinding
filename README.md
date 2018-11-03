**Advanced Lane Finding Project**

---


The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./test_out/archive/000_cv2:imread.png "original"
[image2]: ./test_out/archive/001_undistorted.png "undistorted"
[image3]: ./test_out/archive/002_warped.png "warped"
[image4]: ./test_out/archive/003_hls+lab.png "hls+lab"
[image5]: ./test_out/archive/004_lane_image.png "lane_image"
[image6]: ./test_out/archive/006_merged.png "Output"
[image7]: ./test_out/archive/007_annotated_blended_img.png "annotated and blended"
[image8]: ./test_out/archive/feedback_1_chessboard.png "chessboard w/o detected corners"
[image9]: ./test_out/archive/feedback_1_chessboard_corners_drawn.png "with detected corners"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

This document

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

**A note on code organization and how it was developed**:
The code was mostly developed in regular python scripts with most of the intermediate steps preserved in the **unit_tests/** directory. As patterns emerged and general classes of things became clear a few modules were developed:

 - **camera.py**: camera specific functionality(probably should be folded into util.py)
 - **ImgSaver.py**: provides a **ImgSaver** class whose constructor creates a times tamped subdirectory of **test_out/** and saves files with a name decorated with an index(so they sort conveniently) and provides a **save()** method
 - **ImgUtil.py**
	 - provides interfaces to Open CV routines using my classes so I can enforce what I think should be happening with assert (see for example **cv2CvtColor**), Being new to Open CV this helped me avoid errors which would probably be obvious to people more experienced with the library.
	 - the **Image** class which provides(among other facilities)
		 - **putText**() :  overlays text on an Image (used for position and curvature radius)
		 - **legalColorConversion**(): the original impetus for this class
	 - other utility image funcitons (ex: cb_corners(), hls_lab_lane_detect()
 - **ImgViewer.py**: A debugging aid for myself. While developing a pipline(s) images are pushed into a list in an instance and the show method displays them an M x N gridfull at a time. Most of the routines in this class can be called from pdb to inspect images when things go "walkabout" as they frequently did.
 - **LaneUtils.py** - the heart of the app which provides some non-member functions and the key classes:
	 - **LaneBoundary** which provides
		 - key instance variables:
			 - **x,y**: for the polynomial fit points
			 - **parm_dict**: discussed later in the file where it originates
			 - **radius_of_curvature_m**(): in meters
			 - **fit_polynomial**()
			 - **draw**()
		 - **Window**: encapsulates the sliding window operations
		 - **Lane**
			 - **lane_finder_pipe**() - what the whole lesson is about
			 - **get_image**() - badly named. gets and image of the lane boundaries filled in to be overlaid on the input image
			 - **display_vehicle_pos**()
			 - **show_vehicle_pos**()
			 - **find_pixels_all_boundaries**() - also badly named. drives the sliding window algorithm
		 - **VideoCtrl**
			 - __init__(): sets up the video processing
			 - **process_frame_bp**(): runs each frame through the lane finding pipeline. "bp" refers to the try/except that makes it "bulletproof"
		 - **parm_dict.py** which defines two dictionaries
			 - **parm_dict**: things like 
				 - width and height of the ImageViewer grid described above
				 - parameters for sobel and hough(which ultimately didn't get used much)
				 - thresholds for things we did use like hls, lab, luv
				 - some readable names for a few rgb colors
			 - **cache_dict**: a convenient bag to carry around
				 - calibration matrix
				 - distortion coefficients
				 - lookdown transformation
				 - and it's invers

## camera_setup
In the second code cell in **advanced_lane_finding.ipynb** ("run with the viewer enabled almost everywhere"), we start by calling ut.**app_init**() which:
 - saves the cache_dict(cd) and parm_dict to be passed to the Lane constructor
 - camera_setup() -> **cb_corners**() where
	 - we setup **obj_points** as shown by the OpenCV tutorial code cited in the comments. To oversimplify, obj_points are known by geometry and we calculate the distortion(s) by seeing where they are in the image .vs. where they should be.
	 - then for each image
		 - read the image from disk	
		 - conver it to gray scale
		 - if cv2.**findChessboardCorners**() worked(it fails for 3 images,
			 - append the points we found to the object points
			 - refine  the corners with **cornerSubPix** as suggested at https://docs.opencv.org/3.0-beta/modules/imgproc/doc/feature_detection.html#cornersubpix
	 - finally the **cache_dict** returned from cb_corners() now contains **obj_points** and **img_points** that we pass to **calibrateCamera**()
The pre and post corner detection images look like

![alt text][image8]

![alt text][image9]

We then call cv2.**getPerspectiveTransform**() (twice) to calculate the matrix **M** to transform from camera image to "birds eye" and **M_inv** to do the reverse

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.
undistort() in ImgUtil.py calls cv2Undistort*() -> cv2.undistort() using the mtx and dist discussed above to produce the undistorted imag. One of the interesting, to me, aspects was the tutorial on calculating object points from https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html.  I spent a bunch of time, likely too much to understand this.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image1]

**magic happens** and we get
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at lines # through # in `another_file.py`).  Here's an example of my output for this step.  (note: this is not actually from one of the test images)

First we warp the image into a top down view (see **lane_finder_pipe**())
![alt text][image3]

then via **hls_lab_lane_detect**() in ImgUtil.py we get
![alt text][image4]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

the source and destination points from which the M_lookdown matrix is calculated are hardcoded from the lesson in ImgUtil.py::lookdownXform_src() and lookDownXform_dst() which are passed to look_down() which calls cv2WarpPerspective()

Both images in section 2 (above) show results after the perspective transform.

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?
In LaneUtils.py, find_pixels_all_bndrys() runs the sliding window algorithm for the left and right lanes. lane_finder_pipe() then calls fit_polynomial() on the left and right lane boundaries. It was some small amount of fun to get the points from the two lane boundaries ordered properly in fill_poly_points() to avoid the "bowtie effect" where, in the default order, you wind up with the top point of each boundary connected to the bottom of the other. See the comments for more about that.

The visual result, using the lane lines to define a polygon which we fill, is:

![alt text][image5]



#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

Near the end of lane_finder_pipe() -> display_curve_rad() -> radius_of_curvature_m() we perform the calculations from the lessons as stated in the comments

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

Near the end of lane_finder_pipe() -> display_curve_rad() -> radius_of_curvature_m() we perform the calculations from the lessons as stated in the comments

![alt text][image7]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Links to my video results
-  [project video](https://github.com/evtHsa/sdcAdvLaneFinding/blob/master/test_out/archive/project_video.mp4)
-  [challenge video](https://github.com/evtHsa/sdcAdvLaneFinding/blob/master/test_out/archive/challenge_video.mp4)
-  [harder challenge video](https://github.com/evtHsa/sdcAdvLaneFinding/blob/master/test_out/archive/harder_challenge_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

How burdensome is the guidance to be brief? Grievous. But anyway 

 - shadows clearly give my implementation screaming blue fits
 - the wall in the challenge video played havoc with my implementation as but ?maybe? combining sobel gradients with the hls+lab might have worked better?
 - oddly enough, at least to me, my implementation did FAR better on the harder challenge video than the challenge video
 - most beneficial for my implementation would be not being confusd by the dark/light transition from the wall shadow
 - dealing with shadow mght require changing thresholds perhaps guided by a metric for scene brightness so that transition from bright to shadow as well as daylight -> dusk -> night -> twilight -> daylight would be seamless
 - when my implementation was confused it just returned the input frame and reported the stats in the ipynb of how many frames confused it
