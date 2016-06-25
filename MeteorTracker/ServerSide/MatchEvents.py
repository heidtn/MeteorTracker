import sqlite3
import datetime
import math

"""
@author(s): Nathan Heidt

This parses the meteor events and detects simulataneous events

TODO:
    - This is linked to work on the local database, when porting this over to the server, link it to work with whatever local DB is there

CHANGELOG:
    - 
"""

databasePath = '../Database/local.db'
dbTable = 'events'

#max delay (seconds) between meteor events before we section them
#this really only works with small sample sizes
maxDelay = 5.0
#what is the furthest two observers could see the same meteories (km)
maxDistance = 1000.0

def main():
	meteorEvents = getAllEvents()
	sectionedEvents = sectionMeteorEvents(meteorEvents)


def sectionMeteorEvents(meteorEvents):
	for i in range(len(meteorEvents)):
		meteorEvents[i]['date'] = datetime.datetime.strptime(meteorEvents[i]['date'], "%Y-%m-%dT%H:%M:%S.%f")

	meteorEvents = sorted(meteorEvents, key=lambda k: k['date'])

	sectionedEvents = []
	section = []
	for i in range(len(meteorEvents) - 1):
		if(len(section) > 0):
			if (meteorEvents[i]['date'] - section[-1]['date']).total_seconds() > maxDelay:
				sectionedEvents.append(section)
				section = []

			section.append(meteorEvents[i])
		else:
			section.append(meteorEvents[i])

	return sectionedEvents


#use haversine formula to find great circle distance
def distanceBetweenCoords(lat1, lon1, lat2, lon2):
	earthRadius = 6371.0 #earths radius in km
	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)
	deltaPhi = math.radians(lat2 - lat1)
	deltaLambda = math.radians(lon2 - lon1)

	a = math.sin(deltaPhi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*(math.sin(deltaLambda/2.0)**2)
	c = 2.0*math.atan2(math.sqrt(a), math.sqrt(1 - a))
	d = earthRadius*c

	return d



#this just turns the table into a list of dictionaries for ease of use
def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

#we're not worried about too many items as even 100000 meteor events (vastly unlikely) isn't that large
def getAllEvents():
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