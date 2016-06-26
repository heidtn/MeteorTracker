from .. import camera
import cv2
from .. import find_events
from .. import save_event

"""
@author(s): Nathan Heidt

This is a quick functionality test to ensure different elements are working.

TODO:
    - 
"""

# instantiate the camera, logger, and meteor finder
cam = camera.Camera()
logger = save_event.EventLogger()
finder = find_events.EventFinder()

while True:
    current_image = cam.get_frame()
    previous_image = cam.get_previous_frame()

    keypoints, im_with_keypoints = finder.find_motion_anomaly(
                                                    current_image, 
                                                    previous_image
                                                )

    cv2.imshow('Current image', current_image)
    cv2.imshow('Image with keypoints', im_with_keypoints)

    # if we've detected anomalies
    if(len(keypoints) > 0):
        logger.add_event(current_image, previous_image)

    if(cv2.waitKey(0) & 0xFF == 32):
        break

cv2.destroyAllWindows()
