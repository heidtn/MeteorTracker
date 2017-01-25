import numpy as np

"""
@author(s): Nathan Heidt

This is used to transform vectirs from earth space to camera space to ...space...space.
The goal is to use the vectors to calculate interesections and intersections probabilities

in terms of coordinates:
  Z origin: points towards north pole
  X origin: points towards 0 degrees longitude, 0 degrees latitude
  Y origin: points towards +90 degrees longitude, 0 degrees latitude

TODO:
    - 

CHANGELOG:
    -
"""


earthRadius = 6371.0  # earths radius in km


def get_Rx(theta):
  """
    returns homogenous rotation matrix around x

    Parameters
    ----------
    theta : float
        angle in radians
  """
  return np.matrix([[1.,            0.,               0.,      0.], 
                   [0.,      np.cos(theta), -np.sin(theta),   0.], 
                   [0.,      np.sin(theta), np.cos(theta),    0.],
                   [0.,               0.,      0.,            1.]])

def get_Ry(theta):
  """
    returns homogenous rotation matrix around y

    Parameters
    ----------
    theta : float
        angle in radians
  """
  return np.matrix([[np.cos(theta),  0., np.sin(theta),   0.], 
                   [     0.,         1.,       0.,       0.], 
                   [-np.sin(theta), 0., np.cos(theta),   0.],
                   [      0.,               0.,      0., 1.]])

def get_Rz(theta):
  """
    returns homogenous rotation matrix around z

    Parameters
    ----------
    theta : float
        angle in radians
  """
  return np.matrix([[np.cos(theta), -np.sin(theta), 0.,   0.], 
                   [np.sin(theta),  np.cos(theta), 0.,   0.], 
                   [      0.,               0.,    1.,   0.],
                   [      0.,               0.,    0.,   1.]])

def get_T(x, y, z):
  return np.matrix([[1., 0., 0., x], 
                    [0., 1., 0., y], 
                    [0., 0., 1., z],
                    [0., 0., 0., 1.]])

def get_H(R, t):
  H = R*t
  return H

def get_earth_matpos(evt):
  """
    takes an event with a latitude and longitude and calculates the new position
    where z is pointing north, y and z are orthogonal to ground, and x is straight
    in and out.  Also returns the transform from earth center to the camera.
  """

  latitude = np.deg2rad(-evt.latitude)
  longitude = np.deg2rad(evt.longitude)

  Rz = get_Rz(longitude)
  Ry = get_Ry(latitude)

  # this should be changed to be the total difference from center of earth
  # TODO: use an API to determine true distance from earth center
  T = get_T(earthRadius, 0., 0.)

  # First rotate then transform along new direction
  H_0 = Rz*Ry
  H_1 = T

  # Calculate position
  pos = H_0*H_1*np.matrix([0, 0, 0, 1]).T

  return pos, H_0*H_1

def get_cam_matpos(world_homography, evt):
  """
    takes the world_homography from get_earth_matpos and the event with the cameras
    roll, pitch, and yaw and returns a homography for the camera direction.

    Camera points out alon the Z axis


  """
  # roll around X, left/right of camera
  roll = np.deg2rad(evt.roll)
  # pitch around Y, in/out of camera
  pitch = np.deg2rad(evt.pitch)
  # yaw around Z, up down of camera
  yaw = np.deg2rad(evt.yaw)

  Rx = get_Rx(yaw)
  Ry = get_Ry(pitch)
  Rz = get_Rz(roll)

  camera_homography = Rx*Ry*Rz

  return camera_homography

def get_event_pos(cameraHomography, eventHomography):
  """
    Return a second point in world space in which a meteor event was seen
    takes he position of the camera in world space and a vector, returns
    a second point that lies along the ray of the meteor event.  We may be
    able to even estimate with a single camera the trajectory of the meteor 
    if we can identify the elevation of atmos that meteors flouresce in.
  """

  #camera points out along the Y axis
  T = get_T(0., 1., 0.)

  return cameraHomography*eventHomography*np.matrix([0, 0, 0, 1]).T

def get_intersection(cam1pos, cam1evt, cam2pos, cam2evt):
  """
    takes two rays defined and returns the skew line and seperation distance between them

    If the resulting points are equal the lines perfectly intersect, if the resulting
    points are equal to the original points, then the lines don't have a skew line 
    between them

    yoinked from here: http://morroworks.com/Content/Docs/Rays%20closest%20point.pdf
  """

  A = cam1pos[0:3].T
  B = cam2pos[0:3].T

  a = cam1evt[0:3] - cam1pos[0:3]
  b = cam2evt[0:3] - cam2pos[0:3]

  #numpy is being weird about dot products
  a = np.array(a.flatten())[0]
  b = np.array(b.flatten())[0]

  A = np.array(A.flatten())[0]
  B = np.array(B.flatten())[0]


  c = B - A

  
  D = A + a*(-(a.dot(b))*(b.dot(c)) + (a.dot(c))*(b.dot(b)))/ \
            ( (a.dot(a))*(b.dot(b)) - (a.dot(b))*(a.dot(b)))

  E = B + b*( (a.dot(b))*(a.dot(c)) - (b.dot(c))*(a.dot(a)))/ \
            ( (a.dot(a))*(b.dot(b)) - (a.dot(b))*(a.dot(b)))

  return D, E



def main():
  pass

if __name__ == "__main__":
  main()