import sqlite3
import datetime
import math

"""
@author(s): Nathan Heidt

This parses the meteor events and detects simulataneous events

TODO:
    - This is linked to work on the local database, when porting this over to
      the server, link it to work with whatever local DB is there

CHANGELOG:
    -
"""

databasePath = '../database/local.db'
dbTable = 'events'

# Max delay (seconds) between meteor events before we section them
# This really only works with small sample sizes
maxDelay = 60.0
# What is the furthest two observers could see the same meteories (km)
maxDistance = 1000.0


def main():
    meteorEvents = getAllEvents()
    sectionedEvents = sectionMeteorEvents(meteorEvents)


def sectionMeteorEvents(meteorEvents):
    """
    This takes a list of meteor events and sections them into a list of lists
    of events that are likely to be of the same meteor event

    Parameters
    ----------
    meteorEvents : list of dicts
        Essentially a list of the meteor events as described by the database
        columns.  The dictionary key is the name of each database column.
    """

    # Convert the date from string format to datetime format
    for i in range(len(meteorEvents)):
        meteorEvents[i]['date'] = datetime.datetime.strptime(
                                                meteorEvents[i]['date'],
                                                "%Y-%m-%dT%H:%M:%S.%f"
                                            )

    meteorEvents = sorted(meteorEvents, key=lambda k: k['date'])

    sectionedEvents = []
    section = []
    # Here we go through the meteor events, and if there is a sufficiently
    # large gap in time between two events, we can rule out the possiblity 
    # of those events being related
    for evt in meteorEvents:
        if(len(section) > 0):
            current_date = evt['date']
            most_recent_date = section[-1]['date']
            if (current_date - most_recent_date).total_seconds() > maxDelay:
                sectionedEvents.append(section)
                section = []
            section.append(evt)
        else:
            section.append(evt)

    # TODO: do the same as above, but with distance
    return sectionedEvents


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


def dict_factory(cursor, row):
    """
    This is a helper function to create a dictionary using the column names
    from the database as the keys

    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def getAllEvents():
    """
    This gets all logged events from the database.  At this point, we're not
    worried about too many instances being returned.

    """
    events = []
    print("Fetching database tables")
    conn = sqlite3.connect(databasePath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    for row in c.execute("SELECT * FROM %s" % dbTable):
        events.append(row)
    conn.close()    
    print("Found %d events." % len(events))
    return events


if __name__ == "__main__":
    main()
