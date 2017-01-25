import numpy as np
import cv2
import vector_calcs
import event_finder

"""
@author(s): Nathan Heidt

This encapsulates the event class.  This class is reponsible for storing, extracting,
and working on event data.

TODO:
    - Checks on each of the passed parameters

CHANGELOG:
    -
"""

class Event(object):
  def __init__(self, evt):
    """
      This takes a dict of all the necessary event parameters
    """
    self.evt_dict = evt

    #load internal parameters
    self.current_image = evt['current_image']
    self.previous_image = evt['previous_image']

    self.date = evt['date']

    self.latitude = evt['latitude']
    self.longitude = evt['longitude']

    self.roll = evt['roll']
    self.pitch = evt['pitch']
    self.yaw  = evt['yaw']

    self.intrinsic_matrix = np.matrix(evt['intrinsic_matrix']).reshape((3, 3))
    self.distortion_coeff = np.matrix(evt['distortion_coefficient'])

    self.user_key = evt['user_key']

    #any internal calculations done after this line
    self.pos = vector_calcs.get_earth_matpos(self)


  def get_world_homography(self):
    pos, H = vector_calcs.get_earth_matpos(self)
    return H

  def get_cam_homography(self):
    worldH = self.get_world_homography()
    return vector_calcs.get_cam_matpos(worldH, self)

  def get_evt_vector(self, unitVec):
    """
      Takes a unit vector from the camera's reference frame and returns
      a world point where the event was seen
    """

    camH = self.get_cam_homography()
    #convert to homogenous coordinates
    homeVec = np.matrix([unitVec[0], unitVec[1], 1.]).T

    worldPoint = camH*homeVec

    return worldPoint




class Events(object):
  def __init__(self, evts):
    """
      This holds multiple Event types that are all different frames of the same meteor
      from the same camera
    """
    self.evts = evts

    #load all images from events
    imfiles = []
    for evt in evts:
      imfiles.append(evt.previous_image)

    #because of how we store images we must get the last one as well
    imfiles.append(evt[-1].current_image)

    self.images = [cv2.imread(im) for im in imfiles]
    self.timestamps = [evt.date for evt in self.evts]

    #TODO: should Events be a subclass of Event?
    self.latitude = evts[0].latitude
    self.longitude = evts[0].longitude

    self.roll = evts[0].roll
    self.pitch = evts[0].pitch
    self.yaw  = evts[0].yaw

    self.intrinsic_matrix = evts[0].intrinsic_matrix
    self.distortion_coeff = evts[0].distortion_coefficient

    self.user_key = evts[0].user_key

    self.pos = evts[0].pos

    self.camH = evts[0].get_cam_homography()

  def get_events_avg_point(self):
    """
      get the average point in world coordinates of a meteor event as a unit
      vector in world space
    """
    eventFinder = event_finder.EventFinder()
    pts, avg = eventFinder.compile_motion_anomalies(self.images, 
                                                    self.intrinsic_matrix, 
                                                    self.distortion_coefficient
                                                   )

    #convert from pixel coordinates to a world ray
    vec = np.linalg.pinv(self.intrinsic_matrix)*np.matrix([avg[0, 0], avg[0, 1], 1.])

    T = vector_calcs.get_T(vec[0], vec[1], vec[2])
    pt = self.camH*T

    return pt