import cv2
import numpy as np
import scipy.spatial import KDTree


def getStarPointsFromFile(filename):
	image = cv2.imread(filename)
	return getStarPointsFromImage(image)

def getStarPointsFromImage(image):
	params = cv2.SimpleBlobDetector_Params()
 
 	params.blobColor = 255

	# Change thresholds
	params.minThreshold = .5
	params.thresholdStep = 1
	 
	# Filter by Area.
	params.filterByArea = True
	params.minArea = .1
	params.maxArea = 1500000


	#we do basic blob detection to find white stars on a blue/black sky
	detector = cv2.SimpleBlobDetector(params)

	#this finds all of the points that represent stars
	keypts = detector.detect(image)

	#this creates an image with each point circled
	im_with_keypoints = cv2.drawKeypoints(image, keypts, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	#return the array of points as well as an image representing the points (that can be discarded if desired)
	return (keypts, im_with_keypoints)

def createKDTreeFromKeypoints(keypts):
	pts = []
	for keypt in keypts:
		pts.append(keypt.pt)
	tree = KDTree(pts)

