from datetime import datetime
import cv2

class vid_writer:
	def __init__(self, output=None, numframes=120):
		if output is None:
			self.output = datetime.now().isoformat() + ".h264"
		else:
			self.output = output + ".h264"

		self.numframes = numframes
		self.curframes = 0

		self.writer = cv2.VideoWriter(self.output, cv2.CV_FOURCC('H', '2', '6', '4'), 1, (1280, 720))

		if not self.writer.isOpened():
			print "Unable to open video stream"
			raise


	def __del__(self):
		self.writer.release()