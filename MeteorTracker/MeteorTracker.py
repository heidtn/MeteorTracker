import threading
import server
import cv2
import time
import camera
import find_events
import datetime as dt

import ConfigParser

class Tracker(threading.Thread):
	def __init__(self, source = None):
		self.cam = camera.camera(source)
		self.config = ConfigParser.ConfigParser()

				
	def run(self):
		while True:
			curImg = self.cam.getFrame()
			prevImg = self.cam.getPrevFrame()
			keypts, im = find_events.findMotionAnomaly(prevImg, curImg)

			print "new image loaded"
			
			#we have found an anomaly
			if len(keypts) > 0:
				filename = dt.datetime.now().isoformat()	
				filename += '_event'
				filename += '.jpg'
				cv2.imwrite(filename, curImg)

	def getLatestImg(self):
		print "returning image"
		return self.gobal_dict['lastestimage']


if __name__ == "__main__":
	t = Tracker()
	t.run()
