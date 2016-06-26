"""
@author(s): Nathan Heidt, Jean Nassar

This contains the functions responsible for detecting meteor events

TODO:
    - Check for airplanes/satellites/non meteoric anomalies
    - Normalize lighting
    - Check for star shifts to ensure these don't create false positives

"""
import cv2


def draw_keypoints(vis, keypoints, color=(0, 255, 255)):
    for kp in keypoints:
        x, y = kp.pt
        cv2.circle(vis, (int(x), int(y)), 6, color)


def get_blob_detector():
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


def find_motion_anomaly(previous_image, current_image):
    detector = get_blob_detector()
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

    keypoints = detector.detect(dilated_image)

    im_with_keypoints = current_image.copy()
    draw_keypoints(im_with_keypoints, keypoints, (0, 0, 255))

    return keypoints, im_with_keypoints
