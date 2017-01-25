import sys
sys.path.append('../../meteortracker')

import find_events
import numpy as np
import glob
import cv2

def test_ray_finder():
  eventFinder = find_events.EventFinder()

  imageFiles = glob.glob("../testims/test2/*.jpg")
  images = [cv2.imread(im) for im in imageFiles]

  height, width, _ = images[0].shape

  dist = np.matrix([0., 0., 0., 0., 0.])
  intrinsic = np.matrix([[1500, 0, width/2.],[0, 1500, height/2.],[0, 0, 1]])

  pts, avg = eventFinder.compile_motion_anomalies(images, intrinsic, dist)


  avg_ret = np.matrix([avg[0, 0], avg[0, 1], 1.]).T
  imSpace = intrinsic*avg_ret

  distance = np.sqrt((imSpace[0] - 980.2)**2 + (imSpace[1] - 508.8)**2)

  #should be within 8 pixels 
  assert distance < 8.0