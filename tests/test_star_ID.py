import sys
sys.path.append('../MeteorTracker')

import cv2
import numpy as np
import ephem

import parse_stars as ps


image_file = 'images/N40_30W120_35_5999_2015-02-22-1-10-14.jpg'

keypoints, im = ps.get_star_points_from_file(image_file)
image = cv2.imread(image_file)

points = ps.get_brightest_points(keypoints, 70)

im_with_keypoints = cv2.draw_keypoints(
    image,
    points,
    np.array([]),
    (0, 255, 0),
    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)

brightest_stars, quads = ps.index_known_brightest_stars(
    '../MeteorTracker/starnames_ephem.txt',
    '40.5',
    '-120.593332',
    100,
    '2015/02/22 01:10:14'
)

maxx = 0
maxy = 0
for star in brightest_stars:
    if star.az * 300 > maxx:
        maxx = star.az * 300 + 10
    if star.alt * 300 > maxy:
        maxy = star.alt * 300 + 10

print(maxx, maxy)
star_repr = ps.StarRepresentation(maxy, maxx, 300, 300)
star_epr.draw_quads(quads[::])
star_repr.its_full_of_stars(brightest_stars)
star_repr.show_image("stars")

maxx = 0
maxy = 0
for point in points:
    if point.pt[0] > maxx:
        maxx = point.pt[0]*1 + 10
    if point.pt[1] > maxy:
        maxy = point.pt[1]*1 + 10

im_quads = ps.index_image_stars(points,
                                '40.5',
                                '-120.593332',
                                100,
                                '2015/02/22 01:10:14')

from_image = ps.StarRepresentation(maxy, maxx, 1, 1)
from_image.draw_quads(im_quads)
from_image.fill_star_with_points(points)
from_image.show_image("image")

cv2.waitKey(0)

