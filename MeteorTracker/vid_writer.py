from datetime import datetime
import cv2

class vid_writer:
	def __init__(self, output=None, numframes=120):
		self.output = "/home/brizo/Documents/MeteorTracker/MeteorTracker"
		if output is None:
			self.output += datetime.now().isoformat() + ".avi"
		else:
			self.output += output + ".avi"

		print "output file: ", self.output
		self.numframes = numframes
		self.curframes = 0

		fourcc = cv2.cv.FOURCC('I', 'Y', 'U', 'V')
		self.writer = cv2.VideoWriter(self.output, fourcc, 2, (1280, 720))

		
		if not self.writer.isOpened():
			raise Exception("Unable to open video stream")
		

		self.frames = []

	def addFrame(self, frame):
		self.frames.append(frame)
		if len(self.frames) > self.numframes:
			del self.frames[0]

	def writeFramesToVideo(self):
		for f in self.frames:
			self.writer.write(f)


	def __del__(self):
		self.writer.release()