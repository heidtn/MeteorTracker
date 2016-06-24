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
		os.makedirs(dbdir)
		print("creating database directory")
	if not os.path.exists(imdir):
		print("creating image directory")
		os.makedirs(imdir)

if __name__ == "__main__":
	initialize()