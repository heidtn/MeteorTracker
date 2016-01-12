import Queue
import threading
import server
import cv2

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
	__init__(self, glbl_dict):
		self.gobal_dict = glbl_dict
	def run(self):
		while True:
			pass

"""this function takes an image and finds any meteors or other potential anomalies"""
def findAnomalies(curimg, previmg):
	curimg = cv2.to_grayscale

if __name__ == "__main__":
	pass

