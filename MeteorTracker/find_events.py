
import cv2
import numpy as np


"""
@author: Nathan Heidt

This contains the functions responsible for detecting meteor events

TODO:
	- 
CHANGELOG:
	- 
"""

def getBlobDetector():
	# Setup SimpleBlobDetector parameters.
	params = cv2.SimpleBlobDetector_Params()
	 
	# Change thresholds
	params.minThreshold = 0
	params.maxThreshold = 90

	# Filter by Area.
	params.filterByArea = False
	params.minArea = 4
	params.maxArea = 10000
	 
	# Filter by Circularity
	params.filterByCircularity = False
	params.minCircularity = 0.1
	 
	# Filter by Convexity
	params.filterByConvexity = False
	params.minConvexity = 0.0
	 
	# Filter by Inertia
	params.filterByInertia = True
	params.maxInertiaRatio = .5
	params.minInertiaRatio = 0

	params.filterByColor = False

	# Create a detector with the parameters
	ver = (cv2.__version__).split('.')
	if int(ver[0]) < 3 :
		detector = cv2.SimpleBlobDetector(params)
	else : 
		detector = cv2.SimpleBlobDetector_create(params)

	return detector


def findMotionAnomaly(previmg, curimg):
	detector = getBlobDetector()
	# Our operations on the frame come here
	gray1 = cv2.cvtColor(previmg, cv2.COLOR_BGR2GRAY)
	gray2 = cv2.cvtColor(curimg, cv2.COLOR_BGR2GRAY)

	gray1 = cv2.GaussianBlur(gray1, (3, 3), 0)
	gray2 = cv2.GaussianBlur(gray2, (3, 3), 0)

	diff = cv2.absdiff(gray1, gray2)
	thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)

	keypts = detector.detect(thresh)

	im_with_keypoints = cv2.drawKeypoints(thresh, keypts, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	
	return (keypts, im_with_keypoints)