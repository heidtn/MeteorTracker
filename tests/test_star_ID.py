import sys
sys.path.append('../MeteorTracker')
import parse_stars as ps
import cv2

keypts, im = ps.getStarPointsFromFile('images/N40_30W120_35_5999_2015-02-22-1-10-14.jpg')

cv2.imshow("Keypoints", im)
cv2.waitKey(0)

kdtree = ps.createKDTreeFromKeypoints(keypts)