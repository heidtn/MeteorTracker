import math
import numpy as np
import cv2

from .. import find_events

class Triangulator(object):
	def __init__(self, evtslist):
		"""
			This class encapsulates triangulating the meteor events
		"""
		self.event_finder = find_events.EventFinder()
		self.events = evtslist

	def closest_intersection(self):
		"""
		Given one or more events, draw a ray in their direction.  Return the length
		of their closest intersection
		"""


	def approximate_position(self):
		pass	



#TODO: EVENTS SOULD BE A CLASS THIS IS BAD
def images_from_event(evt):
	"""
		extract the images from an event into an array of cv images.  
	"""
	imfiles1 = []

	for evt in evt1:
		imfiles.append(evt['previous_image'])

	#because of how we store images we must get the last one as well
	imfiles.append(evt[-1]['current_image'])

	ims = [cv2.imread(im) for im in imfiles]

	return ims

#TODO: EVENTS SHOULD BE A CLASS WHY AM I DOING THIS
def get_intrinsic(evt):
	intrinsic = np.matrix(evt['intrinsic_matrix'])
	intrinsic.reshape((3, 3))

def average_ray(evt1, evt2):
	"""
		Given two events, find the average ray for each event and then calculate
		the intersection of those average rays.  This is used to see if two events
		could have seen the same meteor.
	"""
	eventFinder = find_events.EventFinder()

	ims1 = images_from_event(evt1)
	ims2 = images_from_event(evt2)

	intrinsic1 = get_intrinsic(evt1)
	intrinsic2 = get_intrinsic(evt2)

	dist1 = np.matrix(evt1['distortion_coefficient'])
	dist2 = np.matrix(evt2['distortion_coefficient'])


	pts, avg1 = eventFinder.compile_motion_anomalies(ims1, intrinsic1, dist1)
	pts, avg2 = eventFinder.compile_motion_anomalies(ims2, intrinsic2, dist2)


