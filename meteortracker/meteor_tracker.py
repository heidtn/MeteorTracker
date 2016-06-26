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
    """
    A class for running and managing the primary meteor detection tasks.

    Parameters
    ----------
    source : str, optional
        If given a the path of a video file, this will use that.  Otherwise
        it will use the primary camera.

    Attributes
    ----------
    cam : Camera
        This is used to either access the camera or a video file stream
    config : ConfigParser
        This is to parse the config file for different user settings
    event_logger : EventLogger
        When an event is detected, the images are passed to this class for
        logging
    event_finder : EventFinder
        This class is in charge of viewing images to actually find the
        events themselves.
    """
    def __init__(self, source=None):
        self.cam = camera.Camera(source)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.event_logger = save_event.EventLogger()
        self.event_finder = find_events.EventFinder()

    def run(self):
        """
        Run the meteor tracker program.  If a potential meteor is detected,
        log the result.

        """
        while True:
            current_image = self.cam.get_frame()
            previous_image = self.cam.get_previous_frame()

            # detect number of anomalies (keypoints) and highlight them in im
            keypoints, im = self.event_finder.find_motion_anomaly(
                                                            previous_image,
                                                            current_image
                                                        )

            # we have found an anomaly
            if keypoints:
                print("Anomaly found!")
                self.eventLogger.add_event(curImg, prevImg)

if __name__ == "__main__":
    Tracker().run()
