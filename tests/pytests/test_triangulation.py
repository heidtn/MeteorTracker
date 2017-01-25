import sys
sys.path.append('../../meteortracker')
sys.path.append('../../meteortracker/serverside')

import triangulate_events
import events
import vector_calcs

def test_intersection():
  # camera at 0,0 pointing north
  testEvt = create_empty_event()
  testEvt.latitude = 1.
  testEvt.longitude = 0.

  testEvt.roll = 0.
  testEvt.pitch = 0.
  testEvt.yaw = 180.

  camVec = [0, 0, 1]

  evtVector = testEvt.get_evt_vector(camVec)
  

  testEvt2 = create_empty_event()
  testEvt2.latitude = -1.
  testEvt2.longitude = 0.

  testEvt2.roll = 0.
  testEvt2.pitch = 0.
  testEvt2.yaw = 0.

  camVec = [0, 0, 1]

  evtVector2 = testEvt2.get_evt_vector(camVec)
  

  print "\n", testEvt.pos, "\n"
  print evtVector, "\n",
  print testEvt2.pos, "\n"
  print evtVector2, "\n"
  print vector_calcs.get_intersection(testEvt.pos, evtVector, testEvt2.pos, evtVector2)

  


def create_empty_event(keyvalpairs=None):
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
  if keyvalpairs is not None:
    for pair in keyvalpairs:
      event[pair[0]] = pair[1]

  evt = events.Event(event)
  return evt