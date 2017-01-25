import sys
sys.path.append('../../meteortracker/serverside')
sys.path.append('../../meteortracker')

import events
import match_events
import datetime

import random

def test_get_events():
  evts = match_events.getAllEvents()

def test_section_events():
  evtList = []
  time = datetime.datetime.utcnow()

  for i in xrange(5):
    evt = create_empty_event()
    evt.date = time
    evtList.append(evt)
    time += datetime.timedelta(seconds=.5)

  time += datetime.timedelta(seconds=8)

  for i in xrange(6):
    evt = create_empty_event()
    evt.date = time
    evtList.append(evt)
    time += datetime.timedelta(seconds=.5)

  sectionedEvents = match_events.sectionMeteorEvents(evtList)

  #should only be one user
  assert len(sectionedEvents) == 1

  lst = sectionedEvents[evtList[0].user_key]

  assert len(lst) == 2
  assert len(lst[0]) == 5
  assert len(lst[1]) == 6


def test_match_meteor_events():
  evtList = []
  time = datetime.datetime.utcnow()

  for i in xrange(3):
    evt = create_empty_event()
    evt.date = time
    evtList.append(evt)

    evt = create_empty_event()
    evt.user_key = "blorp"
    evt.date = time + datetime.timedelta(seconds = .25 - random.random()/2.)

    evtList.append(evt)
    time += datetime.timedelta(seconds=.5)


  time += datetime.timedelta(seconds=8)

  for i in xrange(2):
    evt = create_empty_event()
    evt.date = time
    evtList.append(evt)
    time += datetime.timedelta(seconds=.5)

  time += datetime.timedelta(seconds=8)

  for i in xrange(2):
    evt = create_empty_event()
    evt.date = time
    evt.user_key = "blorp"
    evtList.append(evt)
    time += datetime.timedelta(seconds=.5)

  sectionedEvents = match_events.sectionMeteorEvents(evtList)
  matchedEvents = match_events.matchMeteorEvents(sectionedEvents)

  assert len(matchedEvents) == 3
  assert len(matchedEvents[0]) == 2
  assert len(matchedEvents[0][0]) == 3
  assert len(matchedEvents[1]) == 1
  assert len(matchedEvents[1][0]) == 2


def create_empty_event():
  event = {'bearing': 0.0, 
           'user_key': 'C0Dfd890', 
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