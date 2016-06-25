import sqlite3


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

#max delay between meteor events before we section them
#this really only works with small sample sizes
maxDelay = 10

def main():
	meteorEvents = getAllEvents()
	sectionedEvents = sectionMeteorEvents(meteorEvents)


def sectionMeteorEvents(meteorEvents):
	#first sort by date.  Dates are isostring format, so alphabetical order sort works
	meteorEvents = sorted(meteorEvents, key=lambda k: k['date'])


	
	

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

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