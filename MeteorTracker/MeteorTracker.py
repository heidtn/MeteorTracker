import threading
import server
import cv2
import time
import camera
import find_events
import datetime as dt

#technically thread safe, but a lazy solution
sharedDict = dict()

"""can be used as a decorator for threadsafe functions"""
def threadsafe_function(fn):
	lk = threading.Lock()
	def new(*args, **kwargs):
		lock.acquire()
		try:
			r = fn(*args, **kwargs)
		except Exception as e:
			raise e
		finally:
			lk.release()
		return r
	return new

class Tracker(threading.Thread):
	def __init__(self, glbl_dict):
		super(Tracker, self).__init__()
		self.gobal_dict = glbl_dict
		self.cam = camera.camera()		
	def run(self):
		while True:
			curImg = self.cam.getFrame()
			prevImg = self.cam.getPrevFrame()
			keypts, im = find_events.findMotionAnomaly(prevImg, curImg)
			self.gobal_dict['lastestimage'] = im

			if len(keypts) > 0:
				filename = dt.datetime.now().isoformat() + '.jpg'
				cv2.imwrite(filename, curImg)

	def getLatestImg(self):
		print "returning image"
		return self.gobal_dict['lastestimage']


