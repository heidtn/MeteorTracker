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

def main():
	meteorEvents = getAllEvents()
	

def getAllEvents():
	events = []
	print("Fetching database tables")
	conn = sqlite3.connect(databasePath)
	c = conn.cursor()
	for row in c.execute("SELECT * FROM %s" % dbTable):
		events.append(row)
	conn.close()	
	print("Found %d events." % len(events))
	return events




if __name__ == "__main__":
	main()