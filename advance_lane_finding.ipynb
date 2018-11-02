{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Self-Driving Car Engineer Nanodegree\n",
    "\n",
    "\n",
    "## Project: **Finding Lane Lines on the Road** \n",
    "***\n",
    "In this project, you will use the tools you learned about in the lesson to identify lane lines on the road.  You can develop your pipeline on a series of individual images, and later apply the result to a video stream (really just a series of images). Check out the video clip \"raw-lines-example.mp4\" (also contained in this repository) to see what the output should look like after using the helper functions below. \n",
    "\n",
    "Once you have a result that looks roughly like \"raw-lines-example.mp4\", you'll need to get creative and try to average and/or extrapolate the line segments you've detected to map out the full extent of the lane lines.  You can see an example of the result you're going for in the video \"P1_example.mp4\".  Ultimately, you would like to draw just one line for the left side of the lane, and one for the right.\n",
    "\n",
    "In addition to implementing code, there is a brief writeup to complete. The writeup should be completed in a separate file, which can be either a markdown file or a pdf document. There is a [write up template](https://github.com/udacity/CarND-LaneLines-P1/blob/master/writeup_template.md) that can be used to guide the writing process. Completing both the code in the Ipython notebook and the writeup template will cover all of the [rubric points](https://review.udacity.com/#!/rubrics/322/view) for this project.\n",
    "\n",
    "---\n",
    "Let's have a look at our first image called 'test_images/solidWhiteRight.jpg'.  Run the 2 cells below (hit Shift-Enter or the \"play\" button above) to display the image.\n",
    "\n",
    "**Note: If, at any point, you encounter frozen display windows or other confounding issues, you can always start again with a clean slate by going to the \"Kernel\" menu above and selecting \"Restart & Clear Output\".**\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import util as ut\n",
    "import ImgViewer as iv\n",
    "import cv2\n",
    "import numpy as np\n",
    "# ImgUtil provides all utility functions for image manipulation\n",
    "import ImgUtil as iu\n",
    "# image view provides a mechanism(mostly for debug)to push images as a pipeline is being developed and \n",
    "# see then 3 x 3 or more at a time \n",
    "import ImgViewer as iv\n",
    "# LaneUtils implements the core of our object model and various \"lane focused\" things\n",
    "# Lanes:  contain LaneBoundary(s) and attributes common to both boundaries\n",
    "# LaneBoundary(s): contain attributes for a particular lane bounday\n",
    "# Windows: are used to calculate lane boundariesimport LaneUtils as lu\n",
    "import LaneUtils as lu"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "findChessboardCorners(camera_cal/calibration5.jpg) failed\n",
      "findChessboardCorners(camera_cal/calibration1.jpg) failed\n",
      "findChessboardCorners(camera_cal/calibration4.jpg) failed\n",
      "WARNING: only using 1 files from test_images/\n",
      "check the test_out directory\n"
     ]
    }
   ],
   "source": [
    "#\n",
    "# run with the viewer enabled almost everywhere to see the output of each stage of the image pipeline\n",
    "#\n",
    "\n",
    "#cd is cache_dict, pd is parm_dict\n",
    "cd, pd = ut.app_init(viewer=True, saver=True, title=\"whatever\")\n",
    "vwr = cd['viewer']\n",
    "\n",
    "def doit():\n",
    "    lane = lu.Lane(cd, pd, vwr=vwr)\n",
    "\n",
    "    for path in ut.get_fnames(\"test_images/\", \"*.jpg\", max=1): # stop at 1 iter to gather pipe stages 4 writepup\n",
    "        in_img = iu.imRead(path, reader='cv2', vwr=vwr)\n",
    "        out_img= lane.lane_finder_pipe(in_img, cd, pd, vwr=vwr)\n",
    "    print(\"check the test_out directory\")\n",
    "\n",
    "doit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "findChessboardCorners(camera_cal/calibration5.jpg) failed\n",
      "findChessboardCorners(camera_cal/calibration1.jpg) failed\n",
      "findChessboardCorners(camera_cal/calibration4.jpg) failed\n",
      "processing project_video.mp4\n",
      "[MoviePy] >>>> Building video test_out/project_video.mp4\n",
      "[MoviePy] Writing video test_out/project_video.mp4\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊| 1260/1261 [02:26<00:00,  8.53it/s]\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[MoviePy] Done.\n",
      "[MoviePy] >>>> Video ready: test_out/project_video.mp4 \n",
      "\n",
      "\n",
      "\n",
      " Total Frames 1261, failed to find lane bounaries in 4 frames\n"
     ]
    }
   ],
   "source": [
    "# the basic video\n",
    "vc = lu.VideoCtrlr(\"project_video\") # th-th-th-th-th-at's all folks. Just one line."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "findChessboardCorners(camera_cal/calibration5.jpg) failed\n",
      "findChessboardCorners(camera_cal/calibration1.jpg) failed\n",
      "findChessboardCorners(camera_cal/calibration4.jpg) failed\n",
      "processing challenge_video.mp4\n",
      "[MoviePy] >>>> Building video test_out/challenge_video.mp4\n",
      "[MoviePy] Writing video test_out/challenge_video.mp4\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 485/485 [04:35<00:00,  1.68it/s]\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[MoviePy] Done.\n",
      "[MoviePy] >>>> Video ready: test_out/challenge_video.mp4 \n",
      "\n",
      "\n",
      "\n",
      " Total Frames 486, failed to find lane bounaries in 458 frames\n"
     ]
    }
   ],
   "source": [
    "vc = lu.VideoCtrlr(\"challenge_video\") "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "findChessboardCorners(camera_cal/calibration5.jpg) failed\n",
      "findChessboardCorners(camera_cal/calibration1.jpg) failed\n",
      "findChessboardCorners(camera_cal/calibration4.jpg) failed\n",
      "processing harder_challenge_video.mp4\n",
      "[MoviePy] >>>> Building video test_out/harder_challenge_video.mp4\n",
      "[MoviePy] Writing video test_out/harder_challenge_video.mp4\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 49%|███████████████████████████████████████████████████████████████████████████████████████████████▊                                                                                                  | 593/1200 [01:33<02:58,  3.41it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 50%|████████████████████████████████████████████████████████████████████████████████████████████████                                                                                                  | 594/1200 [01:34<03:56,  2.56it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 50%|████████████████████████████████████████████████████████████████████████████████████████████████▎                                                                                                 | 596/1200 [01:34<03:32,  2.85it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 50%|████████████████████████████████████████████████████████████████████████████████████████████████▌                                                                                                 | 597/1200 [01:35<04:16,  2.35it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 50%|████████████████████████████████████████████████████████████████████████████████████████████████▋                                                                                                 | 598/1200 [01:36<04:45,  2.11it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 58%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████▎                                                                                | 701/1200 [02:08<01:17,  6.45it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 58%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████▍                                                                                | 702/1200 [02:08<02:25,  3.41it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 59%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏                                                                               | 706/1200 [02:09<01:52,  4.41it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 59%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████▍                                                                               | 708/1200 [02:10<02:16,  3.60it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 59%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████                                                                               | 712/1200 [02:12<02:47,  2.91it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 59%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████▎                                                                              | 713/1200 [02:12<03:23,  2.40it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 60%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████▍                                                                              | 714/1200 [02:13<03:56,  2.06it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 60%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████▌                                                                              | 715/1200 [02:13<04:22,  1.85it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 60%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊                                                                              | 716/1200 [02:14<04:38,  1.74it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 60%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉                                                                              | 717/1200 [02:15<04:46,  1.68it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 60%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████                                                                              | 718/1200 [02:15<04:56,  1.63it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 73%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉                                                    | 878/1200 [02:59<01:07,  4.80it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 76%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▌                                              | 913/1200 [03:05<00:37,  7.66it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 76%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊                                              | 914/1200 [03:06<01:24,  3.40it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 76%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉                                              | 915/1200 [03:07<01:55,  2.46it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 76%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████                                              | 916/1200 [03:07<02:18,  2.06it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 76%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏                                             | 917/1200 [03:08<02:29,  1.90it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 76%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▍                                             | 918/1200 [03:09<02:38,  1.77it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 81%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▋                                    | 975/1200 [03:44<02:54,  1.29it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 83%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▌                                 | 993/1200 [03:47<00:27,  7.55it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 83%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▋                                 | 994/1200 [03:48<01:06,  3.09it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 91%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████                 | 1095/1200 [04:21<00:18,  5.74it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 91%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▎                | 1096/1200 [04:22<00:39,  2.63it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 91%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▍                | 1097/1200 [04:23<00:54,  1.91it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " 95%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▌         | 1141/1200 [04:31<00:15,  3.79it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 95%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▋         | 1142/1200 [04:32<00:24,  2.39it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 95%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊         | 1143/1200 [04:33<00:30,  1.90it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 95%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▉         | 1144/1200 [04:34<00:33,  1.68it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 95%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏        | 1145/1200 [04:34<00:35,  1.56it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 96%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▎        | 1146/1200 [04:35<00:35,  1.51it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 96%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▍        | 1147/1200 [04:36<00:35,  1.48it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\r",
      " 96%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▋        | 1148/1200 [04:37<00:35,  1.47it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "assertion failed\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊| 1199/1200 [04:44<00:00,  6.66it/s]\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[MoviePy] Done.\n",
      "[MoviePy] >>>> Video ready: test_out/harder_challenge_video.mp4 \n",
      "\n",
      "\n",
      "\n",
      " Total Frames 1200, failed to find lane bounaries in 210 frames\n"
     ]
    }
   ],
   "source": [
    "vc = lu.VideoCtrlr(\"harder_challenge_video\") "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "anaconda-cloud": {},
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.2"
  },
  "widgets": {
   "state": {},
   "version": "1.1.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
