"""
@author(s): Nathan Heidt, Jean Nassar

This contains the python classes and functions responsible for star matching
between a known position of stars for a given location and a photograph of stars
for the same or similar locations

TODO:
    - [PLANNED] simple addition, but add planets to the viewable bodies to be
      referenced against.
    - [FIX] the way it's currently set up, the list of quads could potentially
      have repeats of other quads
    - [FIX] the quad classes and image display classes should be consolidated
      either via inheritance or something else

"""
import cv2
import ephem
import numpy as np
from scipy.spatial import KDTree


def get_star_points_from_file(filename):
    image = cv2.imread(filename)
    return get_star_points_from_image(image)


def get_star_points_from_image(image):
    params = cv2.SimpleBlobDetector_Params()

     params.blobColor = 255

    #  Change thresholds
    params.minThreshold = .5
    params.thresholdStep = 1

    #  Filter by Area.
    params.filterByArea = True
    params.minArea = .1
    params.maxArea = 1500000


    # we do basic blob detection to find white stars on a blue/black sky
    detector = cv2.SimpleBlobDetector(params)

    # this finds all of the points that represent stars
    keypoints = detector.detect(image)

    # this creates an image with each point circled
    im_with_keypoints = cv2.drawKeypoints(
        image,
        keypoints,
        np.array([]),
        (0,0,255),
        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    # return the array of points as well as an image representing the points (that can be discarded if desired)
    return keypoints, im_with_keypoints


def get_brightest_points(keypoints, num_indices):
    # sorts the points by size (apparent brightness)
    sorted_points = sorted(keypoints, key=lambda k: k.size)
    # only use the #numIndex brightest points
    return sorted_points[-num_indices:]


def index_known_brightest_stars(filename, lat, lon, elevation, date):
    f = file(filename)
    # we want the star positions for our current observer location to compare against
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    observer.elevation = elevation
    observer.date = date
    brightest_stars = []

    # create ephem body objects for each star name in the file
    for line in f:
        star_name = line.strip('\n')
        star = ephem.star(star_name)
        star.compute(observer)
        if star.alt >= 0:
            brightest_stars.append(star)

    quads = []
    for star in brightest_stars:
        new_quad = StarQuad(star)
        new_quad.find_quad(brightest_stars)
        if new_quad.points_in_unit_circle:
            print(star, "closest stars:", new_quad.quad)
            quads.append(new_quad)

    return brightest_stars, quads


def index_image_stars(keypoints, lat, lon, elevation, date):
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    observer.elevation = elevation
    observer.date = date
    quads = []

    for pt in keypoints:
        new_quad = ImageQuad(pt)
        new_quad.find_quad(keypoints)
        if new_quad.points_in_unit_circle:
            quads.append(new_quad)

    return quads


def create_kd_tree_from_keypoints(keypoints):
    points = []
    for keypoint in keypoints:
        points.append(keypoint.pt)
    tree = KDTree(pts)


def star_distance(star_2, star_1):
    if isinstance(star_1, tuple):
        az_1 = star_1[0]
        alt_1 = star_1[1]
    else:
        az_1 = star_1.az
        alt_1 = star_1.alt

    if isinstance(star_2, tuple):
        az_2 = star_2[0]
        alt_2 = star_2[1]
    else:
        az_2 = star_2.az
        alt_2 = star_2.alt

    az_distance_between = abs(az_1 - az_2)
    if az_distance_between > ephem.pi:
        close_distance = min(az_1, az_2)
        far_distance = max(az_1, az_2)
        az_distance = close_distance + ephem.pi*2.0-far_distance
    else:
        az_distance = az_distance_between

    alt_distance = abs(alt_1 - alt_2)

    dist = np.hypot(az_distance, alt_distance)
    return dist


class StarQuad(object):
    def __init__(self, a_star):
        self.star_A = a_star
        self.quad = []
        self.ac_x = 0
        self.ac_y = 0
        self.ad_x = 0
        self.ad_y = 0
        self.points_in_unit_circle = False

    def find_quad(self, star_list):
        for star in star_list:
            # don't add the star_A to the list
            if star != self.star_A:
                # populate the list first and then sort by closest 3 stars
                if len(self.quad) < 3:
                    self.quad.append(star)
                    self.sort_quad()
                else:
                    # if the current star is closer than a current star in the
                    # quad replace that star
                    if (ephem.separation(self.quad[2], self.star_A)
                        > ephem.separation(star, self.star_A)):
                        self.quad[2] = star
                        self.sort_quad()

        self.points_in_circle()

    def find_farthest(self):
        max_distance = star_distance(self.quad[2], self.star_A)
        bigger_tuple = None
        for i, j in ((0, 1), (0, 2), (1, 2)):
            if star_distance(self.quad[i], self.quad[j]) > max_distance:
                bigger_tuple = (i, j)
                max_distance = star_distance(self.quad[i], self.quad[j])

        if bigger_tuple is not None:
            self.quad[bigger_tuple[0]], self.star_A = (
                self.star_A, self.quad[bigger_tuple[0]])

        self.sort_quad()

    def normalize_quad(self):
        normal = ephem.separation(self.quad[2], self.star_A)

    def points_in_circle(self):
        self.radius = star_distance(self.quad[2], self.star_A) / 2
        self.midpoint = ((self.quad[2].az + self.star_A.az) / 2,
                         (self.quad[2].alt + self.star_A.alt) / 2)

        self.points_in_unit_circle = not (
            star_distance(self.midpoint, self.quad[1]) > self.radius
            or star_distance(self.midpoint, self.quad[0]) > self.radius
        )

    def sort_quad(self):
        self.quad = sorted(self.quad,
                           key=lambda k: star_distance(self.star_A, k))

    def get_star_x(self, star):
        return ephem.twopi - star.az

    def get_star_y(self, star):
        return star.alt


class ImageQuad(object):
    def __init__(self, point):
        self.star_A = point
        self.quad = []
        self.ac_x = 0
        self.ac_y = 0
        self.ad_x = 0
        self.ad_y = 0
        self.points_in_unit_circle = False

    def find_quad(self, keypoints):
        for star in keypoints:
            # don't add the starA to the list
            if star != self.star_A:
                # populate the list first and then sort by closest 3 stars
                if len(self.quad) < 3:
                    self.quad.append(star)
                    self.sort_quad()
                else:
                    # if the current star is closer than a current star in the
                    # quad replace that star
                    if (self.point_distance(self.quad[2], self.star_A)
                            > self.point_distance(star, self.star_A)):
                        self.quad[2] = star
                        self.sort_quad()

        self.find_farthest()
        self.points_in_circle()

    # find star pairs in the quad with the largest separation between them
    def find_farthest(self):
        max_distance = self.point_distance(self.quad[2], self.star_A)
        bigger_tuple = None
        for i, j in ((0, 1), (0, 2), (1, 2)):
            if star_distance(self.quad[i], self.quad[j]) > max_distance:
                bigger_tuple = (i, j)
                max_distance = star_distance(self.quad[i], self.quad[j])

        if bigger_tuple is not None:
            self.star_A, self.quad[bigger_tuple[0]] = (
                self.quad[bigger_tuple[0]], self.star_A)

        self.sort_quad()

    def normalize_quad(self):
        normal = self.point_distance(self.quad[2], self.star_A)

    def points_in_circle(self):
        self.radius = self.point_distance(self.quad[2], self.star_A) / 2

        # convert x, y coords to a keypoint type
        self.midpoint = cv2.KeyPoint(
            (self.quad[2].pt[0] + self.star_A.pt[0]) / 2,
            (self.quad[2].pt[1] + self.star_A.pt[1]) / 2,
            1)

        self.points_in_unit_circle = not (
            self.point_distance(self.midpoint, self.quad[1]) > self.radius
            or self.point_distance(self.midpoint, self.quad[0]) > self.radius
        )

    def point_distance(self, pt1, pt2):
        return np.sqrt((pt1.pt[0] - pt2.pt[0])**2 + (pt1.pt[1] - pt2.pt[1])**2)

    def sort_quad(self):
        self.quad = sorted(self.quad,
                           key=lambda k: np.hypot(self.star_A.pt[0] - k.pt[0],
                                                  self.star_A.pt[1] - k.pt[1]))

    def get_star_x(self, star):
        return star.pt[0]

    def get_star_y(self, star):
        return star.pt[1]



class StarRepresentation(object):
    def __init__(self, height, width, x_scale, y_scale):
        self.width = width
        self.height = height
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.image = np.zeros((height, width, 3), np.uint8)

    def its_full_of_stars(self, star_list):  # Strange name
        for star in star_list:
            x = (ephem.twopi - star.az) * self.x_scale
            y = star.alt * self.y_scale
            self.image[y, x] = (255, 255, 255)

    def fill_star_with_points(self, keypoints):
        for keypoint in keypoints:
            x = keypoint.pt[0]
            y = keypoint.pt[1]
            self.image[y, x] = (255, 255, 255)

    def show_image(self, name):
        cv2.imshow(name, self.image)

    def draw_quads(self, quad_list):
        for quad in quad_list:
            point_A_x = quad.get_star_x(quad.star_A) * self.x_scale
            point_A_y = quad.getstar_y(quad.star_A) * self.y_scale
            color = tuple(np.random.randint(50, 250, 3))
            for star in quad.quad:
                point_x = quad.get_star_x(star) * self.x_scale
                point_y = quad.get_star_y(star) * self.y_scale
                cv2.line(self.image,
                         (int(point_A_x), int(point_A_y)),
                         int(point_x),
                         int(point_y)),
                         color)

    def draw_unit_circles(self, quad_list):
        for quad in quad_list:
            center_x = quad.midpoint[0] * self.x_scale
            center_y = quad.midpoint[1] * self.y_scale
            radius = quad.radius * self.x_scale
            print(radius, quad.radius,
                  float(quad.star_A.alt), float(quad.star_A.az),
                  float(quad.quad[2].alt), float(quad.quad[2].az),
                  float(ephem.separation(quad.star_A, quad.quad[2]))

            color = tuple(np.random.randint(50, 250, 3))
            cv2.circle(self.image,
                       (int(center_x + .5),
                        int(center_y + .5)),
                        int(radius + .5),
                       color)

