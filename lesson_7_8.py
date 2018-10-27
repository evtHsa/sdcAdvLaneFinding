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

cache_dict, parm_dict = ut.app_init(viewer=True, saver=True, title="whatever")
vwr = cache_dict['viewer']

def generate_data(ym_per_pix, xm_per_pix):
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

    # Fit new polynomials to x,y in world space
    left_fit_cr = np.polyfit(ploty*ym_per_pix, leftx*xm_per_pix, 2)
    right_fit_cr = np.polyfit(ploty*ym_per_pix, rightx*xm_per_pix, 2)
    
    return ploty, left_fit_cr, right_fit_cr, leftx, rightx
    
 ####################################################
####################################################
def my_way(ploty, left_fit_cr, right_fit_cr, leftx, rightx):
    cd = cache_dict
    pd = parm_dict
    path = ut.get_fnames("test_images/", "*.jpg")[0]
    init_img, binary_warped = iu.get_binary_warped_image_v2(path, cd, pd, vwr=None)
    # img is just to painlessly fake out Lane ctor
    lane = lu.Lane(cd, pd, img = init_img, units='pixels', vwr=None)
    ut.oneShotMsg("FIXME: units above must be meters")
    lane.ploty = ploty
    lane.left_bndry = lu.LaneBoundary(0, # hope max ix doesnt matter for this test
                                   binary_warped, 'L', lane=lane, vwr=None)
    lane.right_bndry = lu.LaneBoundary(0, # hope max ix doesnt matter for this test
                                    binary_warped, 'R', lane=lane, vwr=None)
    lane.left_bndry.x = leftx
    lane.right_bndry.x = rightx
    lane. left_bndry.fit_coeff = left_fit_cr
    lane. right_bndry.fit_coeff = right_fit_cr
    lane.cd['fit_units'] = 'meters'
    lane. left_bndry.radius_of_curvature()
    lane. right_bndry.radius_of_curvature()
    print("FIXME(meters): "
          + str((lane. left_bndry.curve_radius, lane. right_bndry.curve_radius)))
       
def measure_curvature_real():
    '''
    Calculates the curvature of polynomial functions in meters.
    '''
    # Define conversions in x and y from pixels space to meters
    ym_per_pix = 30/720 # meters per pixel in y dimension
    xm_per_pix = 3.7/700 # meters per pixel in x dimension
    
    # Start by generating our fake example data
    # Make sure to feed in your real data instead in your project!
    ploty, left_fit_cr, right_fit_cr, leftx, rightx = generate_data(ym_per_pix, xm_per_pix)
    my_way(ploty, left_fit_cr, right_fit_cr, leftx, rightx)
    # Define y-value where we want radius of curvature
    # We'll choose the maximum y-value, corresponding to the bottom of the image
    y_eval = np.max(ploty)
    
    # Calculation of R_curve (radius of curvature)
    left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
    right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
    #xm_per_pix, ym_per_pix
    return left_curverad, right_curverad


# Calculate the radius of curvature in meters for both lane lines
left_curverad, right_curverad = measure_curvature_real()

print(left_curverad, 'm', right_curverad, 'm')
# Should see values of 533.75 and 648.16 here, if using
# the default `generate_data` function with given seed number
print("lesson 7.8")
