#!/usr/bin/env python3
#

import util as ut
import ImgViewer as iv
import cv2
import numpy as np
import ImgUtil as iu
import ImgViewer as iv
import LaneUtils as lu

import numpy as np

import numpy as np

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cache_dict['viewer']

def generate_data():
    '''
    Generates fake data to use for calculating lane curvature.
    In your own project, you'll ignore this function and instead
    feed in the output of your lane detection algorithm to
    the lane curvature calculation.
    '''
    # Set random seed number so results are consistent for grader
    # Comment this out if you'd like to see results on different random data!
    np.random.seed(0)
    # Generate some fake data to represent lane-line pixels
    ploty = np.linspace(0, 719, num=720)# to cover same y-range as image
    quadratic_coeff = 3e-4 # arbitrary quadratic coefficient
    # For each y position generate random x position within +/-50 pix
    # of the line base position in each case (x=200 for left, and x=900 for right)
    leftx = np.array([200 + (y**2)*quadratic_coeff + np.random.randint(-50, high=51) 
                                    for y in ploty])
    rightx = np.array([900 + (y**2)*quadratic_coeff + np.random.randint(-50, high=51) 
                                    for y in ploty])

    leftx = leftx[::-1]  # Reverse to match top-to-bottom in y
    rightx = rightx[::-1]  # Reverse to match top-to-bottom in y


    # Fit a second order polynomial to pixel positions in each fake lane line
    left_fit = np.polyfit(ploty, leftx, 2)
    right_fit = np.polyfit(ploty, rightx, 2)
    
    return ploty, left_fit, right_fit

####################################################
####################################################
def my_way(ploty, left_fit, right_fit):
    cd = cache_dict
    pd = parm_dict
    path = ut.get_fnames("test_images/", "*.jpg")[0]
    init_img, binary_warped = iu.get_binary_warped_image_v2(path, cd, pd, vwr=None)
    # img is just to painlessly fake out Lane ctor
    lane = lu.Lane(cd, pd, img = init_img, vwr=None)
    lane.ploty = ploty
    lane.left_bndry = lu.LaneBoundary(0, # hope max ix doesnt matter for this test
                                   binary_warped, 'L', lane=lane, vwr=None)
    lane.right_bndry = lu.LaneBoundary(0, # hope max ix doesnt matter for this test
                                    binary_warped, 'R', lane=lane, vwr=None)
    lane. left_bndry.fit_coeff = left_fit
    lane. right_bndry.fit_coeff = right_fit
    lane.cd['fit_units'] = 'pixels'
    lane. left_bndry.radius_of_curvature('pixels')
    lane. right_bndry.radius_of_curvature('pixels')
    print("FIXME(pixels): "
          + str((lane. left_bndry.curve_radius, lane. right_bndry.curve_radius)))
    lane.cd['fit_units'] = 'meters'
    lane. left_bndry.radius_of_curvature('pixels')
    lane. right_bndry.radius_of_curvature('pixels')
    print("FIXME(meters): "
          + str((lane. left_bndry.curve_radius, lane. right_bndry.curve_radius)))
    
def measure_curvature_pixels():
    '''
    Calculates the curvature of polynomial functions in pixels.
    '''
    # Start by generating our fake example data
    # Make sure to feed in your real data instead in your project!
    ploty, left_fit, right_fit = generate_data() # those are the fit coefficients in my scheme
    my_way(ploty, left_fit, right_fit)
    
    # Define y-value where we want radius of curvature
    # We'll choose the maximum y-value, corresponding to the bottom of the image
    y_eval = np.max(ploty)
    # Calculation of R_curve (radius of curvature)
    left_curverad = ((1 + (2*left_fit[0]*y_eval + left_fit[1])**2)**1.5) / np.absolute(2*left_fit[0])
    right_curverad = ((1 + (2*right_fit[0]*y_eval + right_fit[1])**2)**1.5) / np.absolute(2*right_fit[0])
    return left_curverad, right_curverad


# Calculate the radius of curvature in pixels for both lane lines
left_curverad, right_curverad = measure_curvature_pixels()

print(left_curverad, right_curverad)
# Should see values of 1625.06 and 1976.30 here, if using
# the default `generate_data` function with given seed number
print("lesson 7.7")
