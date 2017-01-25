import sys
sys.path.append('../../meteortracker')

import vector_calcs
import numpy as np
import events

"""
This checks the vector_calcs functions to ensure they are working properly
unit tests
"""


def test_rotations_mats():
  """
    check the rotation matrices to ensure they are correct
  """

  #assert 0 degree rotation
  Rz = vector_calcs.get_Rz(0.0)
  Ry = vector_calcs.get_Ry(0.0)
  Rx = vector_calcs.get_Rx(0.0)
  assert False not in np.isclose(np.identity(4), Rz*Ry*Rx)

  #rotate unit vector in x 90 degrees around z
  T = vector_calcs.get_T(0., 0., 0.)
  Rz = vector_calcs.get_Rz(np.pi/2.0)
  H_1 = vector_calcs.get_H(Rz, T)
  newVec = H_1*np.matrix([1, 0, 0, 1]).T
  assert False not in np.isclose(newVec, np.matrix([0, 1, 0, 1]).T)


def test_earth_location():
  """
    check the earth location calculator
  """
  testEvt = create_empty_event()
  pos, H = vector_calcs.get_earth_matpos(testEvt)
  testMat = np.matrix([vector_calcs.earthRadius, 0, 0, 1]).T
  assert False not in np.isclose(pos, testMat)

  testEvt.latitude = 30.
  testEvt.longitude = 0.

  pos, H = vector_calcs.get_earth_matpos(testEvt)
  testMat = np.matrix([[  5.51744785e+03],
                       [  0.00000000e+00],
                       [  3.18550000e+03],
                       [  1.00000000e+00]])
  assert False not in np.isclose(pos, testMat)

  testEvt.latitude = 30.0
  testEvt.longitude = 30.0
  pos, H = vector_calcs.get_earth_matpos(testEvt)
  testMat = np.matrix([[  4.77825000e+03],
                       [  2.75872392e+03],
                       [  3.18550000e+03],
                       [  1.00000000e+00]])
  assert False not in np.isclose(pos, testMat)


def test_camera_unit_vector():
  # camera at 0,0 pointing north sees an event in the center
  testEvt = create_empty_event()
  testEvt.latitude = 0.
  testEvt.longitude = 0.

  testEvt.roll = 0.
  testEvt.pitch = 0.
  testEvt.yaw = 0.

  camVec = [0, 0, 1]

  evtVector = testEvt.get_evt_vector(camVec)
  testMat = np.matrix([[  6.37100000e+03],
                       [  0.00000000e+00],
                       [  1.00000000e+00],
                       [  1.00000000e+00]])


  assert False not in np.isclose(evtVector, testMat)


  # camera at -1,0 pointing south
  testEvt = create_empty_event()
  testEvt.latitude = -1.
  testEvt.longitude = 0.

  testEvt.roll = 0.
  testEvt.pitch = 0.
  testEvt.yaw = 180.

  camVec = [0, 0, 1]

  evtVector = testEvt.get_evt_vector(camVec)
  testMat = np.matrix([[  6.37001221e+03],
                       [  0.00000000e+00],
                       [ -1.12189129e+02],
                       [  1.00000000e+00]])
  
  assert False not in np.isclose(evtVector, testMat)









def test_intersection():
  """
    check intersection calculations
  """

  cam2pos = np.matrix([1, 0, 0])
  cam1pos = np.matrix([0, 0, 0])
  cam1evt = np.matrix([0, 0, 1])
  cam2evt = np.matrix([0, .2, 1])
  pt1, pt2 = vector_calcs.get_intersection(cam1pos, cam1evt, cam2pos, cam2evt)
  pt1test = np.array([ 0.        ,  0.        ,  0.96153846])
  pt2test = np.array([ 0.03846154,  0.19230769,  0.96153846])

  assert False not in np.isclose(pt1, pt1test)
  assert False not in np.isclose(pt2, pt2test)


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
  """
    Checks two floats for near equality (due to floating point errors)
  """
  return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def create_empty_event():
  event = {'bearing': 0.0, 
           'user_key': 
           'C0Dfd890', 
           'yaw': 0.0, 
           'distortion_coefficient': u"'-4.1802327176423804e-001 5.0715244063187526e-001 0. 0. -5.7843597214487474e-001'", 
           'longitude': 0.0, 
           'latitude': 0.0, 
           'intrinsic_matrix': u"'6.5746697944293521e+002 0. 3.1950000000000000e+002 0. 6.5746697944293521e+002 2.3950000000000000e+002 0. 0. 1.'", 
           'pitch': 90.0, 
           'date': u'2016-06-27T18:18:59.120836', 
           'current_image': u'/home/brizo/Documents/MeteorTracker/meteortracker/database/images/_2016-06-27T18:18:59.120836_current.jpg', 
           'roll': 0.0, 
           'previous_image': u'/home/brizo/Documents/MeteorTracker/meteortracker/database/images/_2016-06-27T18:18:59.120836_previous.jpg'}

  evt = events.Event(event)
  return evt

