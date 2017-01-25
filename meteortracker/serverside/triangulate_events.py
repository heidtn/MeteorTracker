import math
import numpy as np
import cv2

import sys
sys.path.append('../')
import events

"""
@author(s): Nathan Heidt

This handles single and multiview triangulation of events

TODO:
    - 

CHANGELOG:
    -
"""

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


def average_ray(evts1, evts2):
	"""
		Given two events, find the average ray for each event and then calculate
		the intersection of those average rays.  This is used to see if two events
		could have seen the same meteor.
	"""

	#TODO: this can probably be encapsulated in the Events class
	eventFinder = find_events.EventFinder()

	ims1 = evts1.images
	ims2 = evts2.images

	intrinsic1 = evts1.intrinsic_matrix
	intrinsic2 = evts2.intrinsic_matrix

	dist1 = evt1.distortion_coefficient
	dist2 = evt2.distortion_coefficient

	pts, avg1 = eventFinder.compile_motion_anomalies(ims1, intrinsic1, dist1)
	pts, avg2 = eventFinder.compile_motion_anomalies(ims2, intrinsic2, dist2)

	pt1 = evts1.get_events_evt_point()
	pt2 = evts2.get_events_evt_point()

	skew1, skew2 = vector_calcs.get_intersection(evts1.pos, pt1,
																							 evts2.pos, pt2)