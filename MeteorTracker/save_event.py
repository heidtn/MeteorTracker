import sqlite3
import ConfigParser

"""
@author: Nathan Heidt

In charge of saving meteor events to either a remote server or on the local machine for debugging or future uploading.

TODO:
    - 

CHANGELOG:
    - 
"""


class EventLogger():
	def __init__(self):
		self.conn = sqlite3.connect('local.db')
		self.config = ConfigParser.ConfigParser()
		
	def addEvent(self, curimg, previmg, parameters):
		pass

	def uploadToRemote(self):
		pass

