**Advanced Lane Finding Project**

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

[image1]: ./test_out/archive/001_undistorted.png "Undistorted"
[image2]: ./test_out/archive/002_warped.png "warped"
[image3]: ./test_out/archive/003_hls lab.png "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

---


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
In the second code cell in **P2.ipynb** ("run with the viewer enabled almost everywhere"), we start by calling ut.**app_init**() which:
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
	 - we then call cv2.**getPerspectiveTransform**() (twice) to calculate the matrix **M** to transform from camera image to "birds eye" and **M_inv** to do the reverse

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 
**

## original image
![enter image description here](https://github.com/evtHsa/sdcAdvLaneFinding/blob/master/test_out/archive/000_cv2:imread.png)
**

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

undistort() in ImgUtil.py calls cv2Undistort*() -> cv2.undistort() using the mtx and dist discussed above
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

As can be seen in ImgUtil.py and the unit_test/ filesk I tried, guided by the lessons, thesholded sobel, thresholded magnitude, directional sobel but did not good results on all test images. Ultimately hls + lab worked best especially on yellow lines.

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warper()`, which appears in lines 1 through 8 in the file `example.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
dst = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 585, 460      | 320, 0        | 
| 203, 720      | 320, 720      |
| 1127, 720     | 960, 720      |
| 695, 460      | 960, 0        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this:

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
