#
# demo code, usually from the lesson excercise
# return images

import pdb
import ImgViewer as iv
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import util as ut
import ImgUtil as iu
import ImgViewer as iv

def pipeline_6_12_hls(path, s_thresh=(170, 255), sx_thresh=(20, 100), vwr=None):
     
     img = iu.img_read(path, vwr)
     
      # Convert to HLS color space and separate the V channel
     hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
     h_channel = hls[:,:,0]
     l_channel = hls[:,:,1]
     s_channel = hls[:,:,2]
     iv._push(vwr, np.squeeze(h_channel), "h_channel", cmap='gray')
     iv._push(vwr, np.squeeze(l_channel), "l_channel", cmap='gray')
     iv._push(vwr, np.squeeze(s_channel), "s_channel", cmap='gray') # shows lines well
     
     # Sobel x
     sobelx = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0) # Take the derivative in x
     abs_sobelx = np.absolute(sobelx) # Abs x drvtv to accentuate lines away from horizontal
     scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
     iv._push(vwr, np.squeeze(scaled_sobel), "scaled_sobel", cmap='gray')
     ##
     
     # Threshold x gradient
     sxbinary = np.zeros_like(scaled_sobel)
     sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1
     
     # Threshold color channel
     s_binary = np.zeros_like(s_channel)
     s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
     iv._push(vwr, np.squeeze(s_binary), "s_binary", cmap='gray')
     # Stack each channel
     color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
     iv._push(vwr, np.squeeze(color_binary), "color_binary", cmap='gray')
     return color_binary

def doit_6_12(path, vwr=None):

     result =pipeline_6_12_hls(path, vwr=vwr)
     # Plot the result
     f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
     f.tight_layout()
     
     ax1.imshow(image)
     ax1.set_title('Original Image', fontsize=40)
     
     ax2.imshow(result)
     ax2.set_title('Pipeline Result', fontsize=40)
     plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)


def pipeline_6_12_mk2(path, color_space_id, s_thresh=(170, 255),
                       sx_thresh=(20, 100), vwr=None):
     
     img = iu.img_read(path, vwr)
     
      # Convert to HLS color space and separate the V channel
     hls = cv2.cvtColor(img, color_space_id)
     ch_0 = hls[:,:,0]
     ch_1 = hls[:,:,1]
     ch_2 = hls[:,:,2]
     iv._push(vwr, np.squeeze(ch_0), "ch_0", cmap='gray')
     iv._push(vwr, np.squeeze(ch_1), "ch_1", cmap='gray')
     iv._push(vwr, np.squeeze(ch_2), "ch_2", cmap='gray') # shows lines well
     
     # Sobel x
     sobelx = cv2.Sobel(ch_1, cv2.CV_64F, 1, 0) # Take the derivative in x
     abs_sobelx = np.absolute(sobelx) # Abs x drvtv to accentuate lines away from horizontal
     scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
     iv._push(vwr, np.squeeze(scaled_sobel), "scaled_sobel", cmap='gray')
     ##
     
     # Threshold x gradient
     sxbinary = np.zeros_like(scaled_sobel)
     sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1
     
     # Threshold color channel
     s_binary = np.zeros_like(ch_2)
     s_binary[(ch_2 >= s_thresh[0]) & (ch_2 <= s_thresh[1])] = 1
     iv._push(vwr, np.squeeze(s_binary), "s_binary", cmap='gray')
     # Stack each channel
     color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
     iv._push(vwr, np.squeeze(color_binary), "color_binary", cmap='gray')
     ut.brk("look about")
     return color_binary

