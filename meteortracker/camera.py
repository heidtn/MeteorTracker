"""
@author(s): Nathan Heidt, Jean Nassar

This creates streaming image instances using a usb camera, pi camera, or even a
video file.

"""
import enum
from fractions import Fraction
import os
import time

import cv2

# we import like this in case we're not on a raspberry pi
try:
    import picamera
    import picamera.array
except ImportError:
    pass


CameraType = enum.Enum('CameraType', 'pi cv custom')


class Camera(object):
    class _Camera(object):
        def __init__(self, source=None):
            self.camera_settings = dict()
            self.previous_frame = None
            self.current_frame = None
            operating_system = os.uname()[-1]

            # if an rpi
            if source is None:
                if 'arm' in operating_system:
                    self.camera_type = CameraType.pi
                else:
                    self.camera_type = CameraType.cv
            else:
                self.camera_type = CameraType.custom

            if self.camera_type == CameraType.pi:
                self.camera = picamera.PiCamera()
                time.sleep(2)
                self.camera.resolution = (1280, 720)
                self.camera.framerate = Fraction(1, 6)
                self.camera.exposure_mode = 'off'
                self.camera.shutter_speed = 6000000
                self.camera.iso = 800
            elif self.camera_type == CameraType.cv:
                self.camera = cv2.VideoCapture(0)
            elif self.camera_type == CameraType.custom:
                self.camera = cv2.VideoCapture(source)

        def get_frame(self):
            if self.camera_type == CameraType.pi:
                with picamera.array.PiRGBArray(self.camera) as stream:
                    self.camera.capture(stream, format='rgb')
                    frame = stream.array
            elif self.camera_type == CameraType.cv:
                ret, frame = self.camera.read()
            elif self.camera_type == CameraType.custom:
                ret, frame = self.camera.read()
            else:
                raise RuntimeError('Cannot get frame: Unknown camera type.')

            self.previous_frame = self.current_frame
            self.current_frame = frame
            return frame

        def get_previous_frame(self):
            if self.previous_frame is None:
                return self.current_frame
            return self.previous_frame

        def __del__(self):
            if self.camera_type != CameraType.pi:
                self.camera.release()

    instance = None

    def __init__(self, source=None):
        if not Camera.instance:
            Camera.instance = Camera._Camera(source)
        else:
            # this doesn't really even matter...
            Camera.instance.source = source

    def __getattr__(self, name):
        return getattr(self.instance, name)
