import os
import cv2
#we import like this in case we're not on a raspberry pi and the package isn't available
try:
	import picamera
	import picamera.array
except Exception:
	pass
import io
import numpy as np
import time
from fractions import Fraction

"""
@author(s): Nathan Heidt

This creates straming image instances using a usb camera, pi camera, or even a video file.

TODO:
    - 

CHANGELOG:
    - 
"""

class camera:
	class __camera:
		def __init__(self, source=None):
			self.camera_settings = dict()
			self.prev_frame = None
			self.cur_frame = None
			oper_sys = os.uname()[-1]
			#if a rpi
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
					frame = stream.array
			elif self.camera_type == 'cvcam':
				ret, frame = self.camera.read()
			elif self.camera_type == 'custom':
				ret, frame = self.camera.read()
			self.prev_frame = self.cur_frame
			self.cur_frame = frame
			return frame

		def getPrevFrame(self):
			if self.prev_frame is None:
				return self.cur_frame
			return self.prev_frame

		def __del__(self):
			if self.camera_type == 'cvcam' or self.camera_type == 'custom':
				self.camera.release()

	instance = None
	def __init__(self, source=None):
		if not camera.instance:
			camera.instance = camera.__camera(source)
		else:
			#this doesn't really even matter...
			camera.instance.source = source

	def __getattr__(self, name):
		return getattr(self.instance, name)
		




			
