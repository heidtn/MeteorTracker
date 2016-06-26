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
    """
    This class handles image source and streams.

    Parameters
    ----------
    source : str, int
        If passed the path to a video file, the Camera class will use that
        as the streaming source.  If passed an integer, the class will use
        the index of the available attached camera devices.

    Attributes
    ----------
    previous_frame : cv2.Image
        This is an OpenCV datatype that holds the previous frame collected
    current_frame : cv2.Image
        This is an OpenCV datatype that holds the current frame
    camera : cv2.VideoCapture
        This class is used as a wrapper to stream frames from a video source
    instance : _Camera
        A singleton instance for camera access.
    camera_type : CameraType
        An enum used to reference the streaming source
    """
    class _Camera(object):
        def __init__(self, source=None):
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
            """
            Gets the next frame from the video stream.  Querying this will
            retrieve a new frame from the device

            """
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
            """
            After get_frame is called, this can be used to access the previous
            frame

            """
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
            Camera.instance.source = source

    def __getattr__(self, name):
        return getattr(self.instance, name)
