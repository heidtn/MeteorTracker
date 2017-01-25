import sqlite3
import datetime
import math
import triangulate_events

import sys
sys.path.append('../')
import events

import settings

"""
@author(s): Nathan Heidt

This parses the meteor events and detects simulataneous events

TODO:
    - This is linked to work on the local database, when porting this over to
      the server, link it to work with whatever local DB is there

CHANGELOG:
    -
"""

databasePath = settings.databasePath
dbTable = 'events'

# Max delay (seconds) between meteor events before we section them
# This really only works with small sample sizes
maxDelay = 5.0

# What is the furthest two observers could see the same meteories (km)
maxDistance = 100.0

# How long (seconds) apart can separate cameras see the same sample
maxTimeBetweenSamples = 5.0


def main():
    meteorEvents = getAllEvents()
    sectionedEvents = sectionMeteorEvents(meteorEvents)
    matchedEvents = matchMeteorEvents(sectionedEvents)

    for event in matchedEvents:
        if(len(event) == 2):
            triangulator = triangulate_events.Triangulator(event[0], event[1])


def compareEvents(evt1, evt2):
    """
    This takes two event lists and performs checks to see if they are possible
    matches of the same meteor
    """

    firstEvt1 = evt1[0]
    firstEvt2 = evt2[0]

    # check time first
    current_date = firstEvt1.date #time of this events first evt
    most_recent_date = firstEvt2.date

    if (current_date - most_recent_date).total_seconds() > maxTimeBetweenSamples:
        return False

    #TODO: encapsulate distance checks in the event class
    # check distance between users
    user1lat = firstEvt1.latitude
    user1lon = firstEvt1.longitude

    user2lat = firstEvt2.latitude
    user2lon = firstEvt2.longitude

    if distanceBetweenCoords(user1lat, user1lon, user2lat, user2lon) > maxDistance:
        return False


    # TODO check the skew line distance between the images
    # need to extract the meteor location in image, the angle from center,
    # the absolute angle from earth center, and then skew line intersection

    return True



def matchMeteorEvents(sectionedEvents):
    """
    This takes the sectioned events from sectionMeteorEvents and pairs 
    possible events together.

    checks:
        - if two users saw an event within some timeframe
        - if those users are within some distance of each other
        - if the skew line distance between their view is minimal

    If the checks pass then it is considered to be the same meteor sighting
    """

    #unroll the users events first [[evt1..],[evt2..],..]
    unrolledEvents = []
    for user in sectionedEvents:
        for evt in sectionedEvents[user]:
            unrolledEvents.append(evt)

    #now sort by time of the first event
    #TODO, maybe average the times then sort by that average instead
    sortedEvents = sorted(unrolledEvents, key=lambda x: x[0].date)

    #compile into sections based on checks
    coincidentEvents = []
    section = []
    for evt in sortedEvents:
        if(len(section) > 0):
            if compareEvents(evt, section[0]) == False:
                coincidentEvents.append(section)
                section = []
            section.append(evt)
        else:
            section.append(evt)
    if len(section) > 0:
        coincidentEvents.append(section)

    return coincidentEvents



def sectionMeteorEvents(meteorEvents):
    """
    This takes a list of meteor events and sections them into a dictionary
    of lists where each key represents a user_key and each list represents
    all the events for that user.

    It then goes through user by user and splits up the single list into
    a list of event frames.  For example a single meteor event make take up 
    2 or more frames of images so they will be put together in a single
    list.

    Here is what this looks like:

    {
        'user_key_1' : [[evt1frame1,evt1frame2,...],[evt2frame1,...],...],
        'user_key_2' : [[evt1frame1,evt1frame2,...],[evt2frame1,...],...],
        ...  
    }

    Parameters
    ----------
    meteorEvents : list of dicts
        Essentially a list of the meteor events as described by the database
        columns.  The dictionary key is the name of each database column.
    
    """

    # TODO: maybe this functionality can be in the Events class instead

    # Create a dictionary where the key is the user_key and the value is a
    # list of that users events
    user_events = {}
    for evt in meteorEvents:
        user_events.setdefault(evt.user_key, [])
        user_events[evt.user_key].append(evt)
    
    # Sort each users events by time
    for key in user_events:
        user_events[key] = sorted(user_events[key], key=lambda k: k.date)


    # Here we go through the meteor events, and if there is a sufficiently
    # large gap in time between two events, we can rule out the possiblity
    # of those events being related.  There are better methods using CV,
    # but this is fast and has very few false negatives
    for key in user_events:
        sectionedEvents = []
        section = []
        for evt in user_events[key]:
            if(len(section) > 0):
                current_date = evt.date
                most_recent_date = section[-1].date
                if (current_date - most_recent_date).total_seconds() > maxDelay:
                    sectionedEvents.append(section)
                    section = []
                section.append(evt)
            else:
                section.append(evt)
        if len(section) > 0:
            sectionedEvents.append(section)
        user_events[key] = sectionedEvents

    # TODO: do the same as above, but with distance
    return user_events


def distanceBetweenCoords(lat1, lon1, lat2, lon2):
    """
    This uses the haversine formula to calculate the great-circle distance
    between two points.

    Parameters
    ----------
    lat1 : float
        The latitude of the first point
    lon1 : float
        The longitude of the first point
    lat2 : float
        The latitude of the second point
    lon2 : float
        The longitude of the second point
    """
    earthRadius = 6371.0  # earths radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    deltaPhi = math.radians(lat2 - lat1)
    deltaLambda = math.radians(lon2 - lon1)

    a = math.sin(deltaPhi/2.0)**2 + \
                 math.cos(phi1)*math.cos(phi2)*(math.sin(deltaLambda/2.0)**2)

    c = 2.0*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earthRadius*c

    return d

def skewLineDistance(evt1, evt2):
    """
    given two events compute the skew line distance between them
    """
    pass

def eventFactory(cursor, row):
    """
    This is a helper function to create a dictionary using the column names
    from the database as the keys

    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    
    #fill an Event type with the dict here
    evt = events.Event(d)
    return evt


def getAllEvents():
    """
    This gets all logged events from the database.  At this point, we're not
    worried about too many instances being returned.

    """
    events = []
    print("Fetching database tables")
    conn = sqlite3.connect(databasePath)
    conn.row_factory = eventFactory
    c = conn.cursor()
    for row in c.execute("SELECT * FROM %s" % dbTable):
        events.append(row)
    conn.close()   
    print("Found %d events." % len(events))
    return events


if __name__ == "__main__":
    main()
