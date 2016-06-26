"""
@author(s): Nathan Heidt, Jean Nassar

This contains the functions responsible for detecting meteor events.  Currently
it uses a simple blob detector on diffed frames.  This works all right in some
situations and tends the catch the majority of actual meteor events.  However,
there can be a lot of false positives when using noisy cameras.

TODO:
    - Check for airplanes/satellites/non meteoric anomalies
    - Normalize lighting
    - Check for star shifts (due to the earths rotation)
      to ensure these don't create false positives on long
      exposure shots

"""
import cv2

class EventFinder(object):
    """
    This class takes in images from a video stream to determine if they
    contain an instance of a meteor

    Attributes
    ----------
    detector : cv2.SimpleBlobDetector
        This is a blob detector algorithm that is used to isolate changes 
        between frames
    """
    def __init__(self):
        self.detector = self.get_blob_detector()

    def draw_keypoints(self, vis, keypoints, color=(0, 255, 255)):
        """
        This function is mostly used for debugging purposes.  Given an image
        it will draw circles on every keypoint it finds.

        Parameters
        ----------
        vis : Image
            The image to draw the circles on
        keypoints : list of cv2.KeyPoints
            This is a list of KeyPoints where events have been detected.
        color : tuple
            color is a tuple of length 3 that specifies the RGB values of 
            the circles
        """
        for kp in keypoints:
            x, y = kp.pt
            cv2.circle(vis, (int(x), int(y)), 6, color)


    def get_blob_detector(self):
        """
        This generates a blob detector based on arbitrary parameters tuned for
        this particular project

        """
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
        params.minThreshold = 0
        params.maxThreshold = 90

        # Filter by Area.
        params.filterByArea = False
        params.minArea = 4
        params.maxArea = 10000

        # Filter by Circularity
        params.filterByCircularity = False
        params.minCircularity = 0.1

        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.0

        # Filter by Inertia (ratio of widest to thinnest point)
        params.filterByInertia = True
        params.maxInertiaRatio = .5
        params.minInertiaRatio = 0

        params.filterByColor = False

        # Create a detector with the parameters
        ver = cv2.__version__.split('.')
        if int(ver[0]) < 3:
            detector = cv2.SimpleBlobDetector(params)
        else:
            detector = cv2.SimpleBlobDetector_create(params)

        return detector


    def find_motion_anomaly(self, previous_image, current_image):
        """
        Given two images, this function compares them to find potential
        meteors.

        Parameters
        ----------
        previous_image : cv2.Image
            The previous image to compare against
        current_image : cv2.Image
            The current image to compare against
        """
        # Our operations on the frame come here
        gray1 = cv2.cvtColor(previous_image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)

        # gaussian to filter out noise
        gray1 = cv2.GaussianBlur(gray1, (3, 3), 0)
        gray2 = cv2.GaussianBlur(gray2, (3, 3), 0)

        diff = cv2.absdiff(gray1, gray2)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        dilated_image = cv2.dilate(thresh, None, iterations=2)

        keypoints = self.detector.detect(dilated_image)

        im_with_keypoints = current_image.copy()
        self.draw_keypoints(im_with_keypoints, keypoints, (0, 0, 255))

        return keypoints, im_with_keypoints
