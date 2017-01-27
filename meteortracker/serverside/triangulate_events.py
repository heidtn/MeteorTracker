import numpy as np
import sys
sys.path.append('../')
import events
import vector_calcs
import find_events

from itertools import combinations

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
        Finds the point of intersection of the average point of each of the events
        """
        # Using some form of matrix decomp would probably be best here, BUT HOW

        pdf = lambda x, u, sig: 1. / np.sqrt(2. * sig * np.pi) * np.exp(-(x - u) ** 2 / (2. * sig))

        averages = []
        sigmas = []
        for comb in combinations(self.events, 2):
            sk1, sk2 = average_ray(comb[0], comb[1])
            dist = vector_calcs.get_distance(sk1, sk2)
            sig = dist / 10.  # arbitrary division so the pdf floats don't get too small

            center = (sk1 + sk2) / 2.

            averages.append(center)
            sigmas.append(sig)

        estimatedCenter = np.array([0, 0, 0])
        for i in xrange(len(averages)):
            estimatedCenter += sigmas[i]*averages[i]

        estimatedCenter /= sum(sigmas)

        return estimatedCenter

    def approximate_position(self):
        pass


def average_ray(evts1, evts2):
    """
        Given two events, find the average ray for each event and then calculate
        the intersection of those average rays.  This is used to see if two events
        could have seen the same meteor.
    """

    # TODO: this can probably be encapsulated in the Events class
    eventFinder = find_events.EventFinder()

    ims1 = evts1.images
    ims2 = evts2.images

    intrinsic1 = evts1.intrinsic_matrix
    intrinsic2 = evts2.intrinsic_matrix

    dist1 = evt1.distortion_coefficient
    dist2 = evt2.distortion_coefficient

    pts, avg1 = eventFinder.compile_motion_anomalies(ims1, intrinsic1, dist1)
    pts, avg2 = eventFinder.compile_motion_anomalies(ims2, intrinsic2, dist2)

    pt1 = evts1.get_evt_vector(avg1)
    pt2 = evts2.get_evt_vector(avg2)

    skew1, skew2 = vector_calcs.get_intersection(evts1.pos, pt1,
                                                 evts2.pos, pt2)

    return skew1, skew2
