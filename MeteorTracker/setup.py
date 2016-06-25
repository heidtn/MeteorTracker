import ConfigParser
import os

"""
@author(s): Nathan Heidt

This initializes necessary directories and files.

TODO:
    - 

CHANGELOG:
    - 
"""

dbdir = 'Database'
imdir = 'Database/images'

def initialize(configPath='config.ini'):
	config = ConfigParser.ConfigParser()
	config.read(configPath)

	if not os.path.exists(dbdir):
		print("creating database directory")
		os.makedirs(dbdir)
	if not os.path.exists(imdir):
		print("creating image directory")
		os.makedirs(imdir)

	dbpath = os.path.abspath(dbdir)
	impath = os.path.abspath(imdir)

	config.set('Database', 'Local', dbpath + '/local.db')
	config.set('Database', 'LocalImages', impath + '/')

	#TODO ask user for geodata
	#TODO calibrate camera

	with open(configPath, 'wb') as configfile:
		config.write(configfile)


if __name__ == "__main__":
	#todo, use argparse to paramaterize setup
	initialize()