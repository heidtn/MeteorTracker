import os
import cv2
try:
	import picamera
	import picamera.array
except Exception:
	pass
import io
import numpy as np
import time
from fractions import Fraction

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
			time.sleep(2)
			self.camera.resolution = (1280, 720)
			self.camera.framerate = Fraction(1, 6)
			self.camera.exposure_mode = 'off'
			self.camera.shutter_speed = 6000000
			self.camera.ISO = 800
		elif self.camera_type == 'cvcam':
			self.camera = cv2.VideoCapture(0)
		elif self.camera_type == 'custom':
			self.camera = cv2.VideoCapture(source)

	def getFrame(self):
		if self.camera_type == 'picam':
			with picamera.array.PiRGBArray(self.camera) as stream:
				self.camera.capture(stream, format='rgb')
				image = stream.array
				print "img returned"
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


			
