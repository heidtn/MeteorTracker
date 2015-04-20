import sys
sys.path.append('../MeteorTracker')
import parse_stars as ps
import cv2
import numpy as np
import ephem

keypts, im = ps.getStarPointsFromFile('images/N40_30W120_35_5999_2015-02-22-1-10-14.jpg')

image = cv2.imread('images/N40_30W120_35_5999_2015-02-22-1-10-14.jpg')

pts = ps.getBrightestPoints(keypts, 70)

im_with_keypoints = cv2.drawKeypoints(image, pts, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#cv2.imshow("Keypoints", im_with_keypoints)
#cv2.waitKey(0)

brightestStars, quads = ps.indexKnownBrightestStars('../MeteorTracker/starnames_ephem.txt', '40.5', '-120.593332', 100, '2015/02/22 01:10:14')

maxx = 0
maxy = 0
for star in brightestStars:
	if star.az*300 > maxx:
		maxx = star.az*300 + 10
	if star.alt*300 > maxy:
		maxy = star.alt*300 + 10

print maxx, maxy
starRepr = ps.starRepresentation(maxy, maxx, 300, 300)
starRepr.drawQuads(quads[0::1])
#starRepr.drawUnitCircles(quads[0::1])
starRepr.itsFullOfStars(brightestStars)
starRepr.showImage("stars")

maxx = 0
maxy = 0
for pt in pts:
	if pt.pt[0] > maxx:
		maxx = pt.pt[0]*1 + 10
	if pt.pt[1] > maxy:
		maxy = pt.pt[1]*1 + 10

imQuads = ps.indexImageStars(pts, '40.5', '-120.593332', 100, '2015/02/22 01:10:14')

fromImage = ps.starRepresentation(maxy, maxx, 1, 1)
fromImage.drawQuads(imQuads)
fromImage.fillStarsWithPts(pts)
fromImage.showImage("image")


cv2.waitKey(0)
