import cv2
import numpy as np
from scipy.spatial import KDTree
import ephem
import random

"""
@author: Nathan Heidt

This contains the python classes and functions responsible for star matching between a known position of stars for a given location and a photograph of stars for the same or similar locations

TODO:
    - [PLANNED]simple addition, but add planets to the viewable bodies to be referenced against.
    - [FIX]the way it's currently set up, the list of quads could potentially have repeats of other quads
CHANGELOG:
    - 
"""

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

def getBrightestPoints(keypts, numIndexes):
	#sorts the points by size (apparent brightness)
	sortedPts = sorted(keypts, key=lambda k: k.size)
	#only use the #numIndex brightest points
	return sortedPts[-numIndexes:]

def indexKnownBrightestStars(filename, lat, lon, elevation, date):
	f = file(filename)
	#we want the star positions for our current observer location to compare against
	observer = ephem.Observer()
	observer.lat = lat
	observer.lon = lon
	observer.elevation = elevation
	observer.date = date
	brightestStars = []

	#create ephem body objects for each star name in the file
	for line in f:
		starname = line.strip('\n')
		star = ephem.star(starname)
		star.compute(observer)
		if(star.alt >= 0):
			brightestStars.append(star)


	quads = []
	for star in brightestStars:
		newquad = starQuad(star)
		newquad.findQuad(brightestStars)
		#if(newquad.pointsInUnitCircle):
			#print star, "closest stars:", newquad.quad
		quads.append(newquad)

	return (brightestStars, quads)


def createKDTreeFromKeypoints(keypts):
	pts = []
	for keypt in keypts:
		pts.append(keypt.pt)
	tree = KDTree(pts)


class starQuad:
	def __init__(self, astar):
		self.starA = astar
		self.quad = []
		self.ac_x = 0
		self.ac_y = 0
		self.ad_x = 0
		self.ad_y = 0
		self.pointsInUnitCircle = False

	def findQuad(self, starlist):
		for star in starlist:
			#don't add the starA to the list
			if star != self.starA:
				#populate the list first and then sort by closest 3 stars
				if len(self.quad) < 3:
					self.quad.append(star)
					self.sortQuad()
				else:
					#if the current star is closer than a current star in the quad replace that star
					if(ephem.separation(self.quad[2], self.starA) > ephem.separation(star, self.starA)):
						self.quad[2] = star
						self.sortQuad()

			print "star, ", float(self.starA.alt), float(self.starA.az)
			for i in self.quad:
				print float(ephem.separation(i, self.starA))

		print self.starA, self.quad

		self.pointsInCircle()

	def normalizeQuad(self):
		normal = ephem.separation(self.quad[2], self.starA)

	def pointsInCircle(self):
		self.radius = float(ephem.separation(self.quad[2], self.starA))/2.0
		self.midpoint = ((self.quad[2].az + self.starA.az)/2.0,(self.quad[2].alt + self.starA.alt)/2.0)
		print "star a az",float(self.starA.az)," star a alt", float(self.starA.alt), " star b az", float(self.quad[2].az)," star b alt", float(self.quad[2].alt), " midpoint:",self.midpoint, "   radius:",self.radius
		print "star c az",(self.quad[1].az)," star c alt", (self.quad[1].alt), " star d az", (self.quad[0].az)," star d alt", (self.quad[0].alt)
		if(ephem.separation(self.midpoint, self.quad[1]) > self.radius or ephem.separation(self.midpoint, self.quad[0]) > self.radius):
			self.pointsInUnitCircle = False
		else:
			self.pointsInUnitCircle = True


	def sortQuad(self):
		self.quad = sorted(self.quad, key=lambda k: ephem.separation(self.starA, k))




class starRepresentation:
	def __init__(self, height, width, xscale, yscale):
		self.width = width
		self.height = height
		self.xscale = xscale
		self.yscale = yscale
		self.image = np.zeros((height,width,3), np.uint8)

	def itsFullOfStars(self, starlist):
		for star in starlist:
			x = star.az*self.xscale
			y = star.alt*self.yscale
			self.image[y,x] = (255, 255, 255)

	def showImage(self):
		cv2.imshow("representation", self.image)
		cv2.waitKey(0)

	def drawQuads(self, quadlist):
		for quad in quadlist:
			pointA_x = quad.starA.az*self.xscale
			pointA_y = quad.starA.alt*self.yscale
			color = (random.randint(50,250),random.randint(50,250),random.randint(50,250))
			for star in quad.quad:
				point_x = star.az*self.xscale
				point_y = star.alt*self.yscale
				cv2.line(self.image, (int(pointA_x), int(pointA_y)),(int(point_x), int(point_y)),color)

	def drawUnitCircles(self, quadlist):
		for quad in quadlist:
			center_x = quad.midpoint[0]*self.xscale
			center_y = quad.midpoint[1]*self.yscale
			radius = quad.radius*self.xscale
			print radius, quad.radius, float(quad.starA.alt), float(quad.starA.az), float(quad.quad[2].alt), float(quad.quad[2].az), float(ephem.separation(quad.starA, quad.quad[2]))
			color = (random.randint(50,250),random.randint(50,250),random.randint(50,250))
			cv2.circle(self.image, (int(center_x + .5), int(center_y + .5)), int(radius + .5), color)
