import server
import cv2
import time
import camera
import find_events
import datetime as dt

import ConfigParser
import save_event


"""
@author(s): Nathan Heidt

This is the primary program for detecting and logging Meteors.  Running python MeteorTracker.py is sufficient.  
Make sure the parameters specified in the config.ini file are correct.

TODO:
    - 

CHANGELOG:
    - 
"""

class Tracker():
	def __init__(self, source = None):
		self.cam = camera.camera(source)
		self.config = ConfigParser.ConfigParser()
		self.config.read('config.ini')
		self.eventLogger = save_event.EventLogger()


	def run(self):
		while True:
			curImg = self.cam.getFrame()
			prevImg = self.cam.getPrevFrame()

			#detect number of anomalies (keypts) and highlight them in im
			keypts, im = find_events.findMotionAnomaly(prevImg, curImg)
			
			#we have found an anomaly
			if len(keypts) > 0:
				self.eventLogger.addEvent(curImg, prevImg)

	def getLatestImg(self):
		print "returning image"
		return self.gobal_dict['lastestimage']


if __name__ == "__main__":
	t = Tracker()
	t.run()
