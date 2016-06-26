"""
@author(s): Nathan Heidt, Jean Nassar

This is the primary program for detecting and logging Meteors. Running
`python meteor_tracker.py` is sufficient.

Make sure the parameters specified in the config.ini file are correct.

"""
import configparser

from . import camera
from . import find_events
from . import save_event


class Tracker(object):
    def __init__(self, source=None):
        self.cam = camera.Camera(source)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.event_logger = save_event.EventLogger()
        self.event_finder = find_events.EventFinder()

    def run(self):
        while True:
            current_image = self.cam.get_frame()
            previous_image = self.cam.get_previous_frame()

            # detect number of anomalies (keypoints) and highlight them in im
            keypoints, im = self.event_finder.find_motion_anomaly(previous_image,
                                                            current_image)

            # we have found an anomaly
            if keypoints:
                print("Anomaly found!")
                self.eventLogger.add_event(curImg, prevImg)

if __name__ == "__main__":
    Tracker().run()
