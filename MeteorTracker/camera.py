import os
import cv2
try:
	import picamera
except Exception:
	pass
import io
import numpy as np

class camera:
	def __init__(self, source=None):
		self.camera_settings = dict()

		oper_sys = os.uname()[-1]
		if 'arm' in oper_sys and source is None:
			self.camera_type = 'picam'
		elif source is None:
			self.camera_type = 'cvcam'
		else:
			self.camera_type = 'custom'

		if self.camera_type == 'picam':
			self.camera = picamera.PiCamera()
		elif self.camera_type == 'cvcam':
			self.camera = cv2.VideoCapture(0)
		elif self.camera_type == 'custom':
			self.camera = cv2.VideoCapture(source)

	def getFrame(self):
		if self.camera_type == 'picam':
			with picamera.PiCamera() as camera:
				self.camera.start_preview()
				time.sleep(2)
				with picamera.array.PiRGBArray(camera) as stream:
					self.camera.capture(stream, format='bgr')
					# At this point the image is available as stream.array
					image = stream.array
					return image
		elif self.camera_type == 'cvcam':
			ret, frame = self.camera.read()
			return frame
		elif self.camera_type == 'custom':
			ret, frame = self.camera.read()
			return frame

	def __del__(self):
		if self.camera_type == 'cvcam' or self.camera_type == 'custom':
			self.camera.release()


			