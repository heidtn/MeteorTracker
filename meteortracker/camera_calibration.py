import cv2
import numpy as np
import time
import camera


"""
@author(s): Nathan Heidt

This program will calibrate the camera.  It will write the distortion
coefficients and camera matrix to the config file.

TODO:
    -

CHANGELOG:
    -
"""

# get at least 30 images at least
numImages = 30


def calibrate_camera():
    """
    This uses the camera to create an intrinsic matrix and distortion
    coefficient for calibrating the camera.  The intrinsic matrix can
    be used to determine true angles and is necessary for triangulation.
    The distortion coefficient is used to straighten out lense distortion like
    that seen in fisheye lenses.

    """
    print("Starting Camera Calibration.  Waiting for image with checkerboard.")
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    numGoodImages = 0

    cam = camera.Camera()
    while numGoodImages < 30:
        im = cam.get_frame()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
        # If found, add object points, image points (after refining them)
        if ret:
            numGoodImages += 1
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,
                                        corners, 
                                        (11, 11), 
                                        (-1, -1), 
                                        criteria
                                        )
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (7, 6), corners2, ret)
            cv2.imshow('img', img)
            print("Found good image %d/%d" % (numGoodImages/numImages))
            cv2.waitKey(500)

    print("Successfully collected images.")
    print("Calculating Matrices...")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, 
                                                       imgpoints, 
                                                       gray.shape[::-1],
                                                       None,
                                                       None
                                                       )
    print("Camera matrix:")
    print(mtx)
    print("\nDistortion Coefficients:")
    print(dist)

    mean_error = 0
    for i in xrange(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], 
                                          rvecs[i], 
                                          tvecs[i], 
                                          mtx, 
                                          dist)
        error = cv2.norm(imgpoints[i], 
                         imgpoints2, 
                         cv2.NORM_L2
                         )/len(imgpoints2)
        tot_error += error

    print("Total reprojection error: {}".format(mean_error/len(objpoints)))

    return matx, dist


def undistort_image(img, camMatrix, distCoeff):
    """
    This can straighten out an image given the intrinsic matrix (camera 
    matrix) and the distortion coefficients.

    Parameters
    ----------
    img : image
        This is the image we wish to undistort
    camMatrix : 2dmatrix
        This is the intrinsic matrix of the camera (3x3)
    distCoeff : 1darray
        This is the distortion coefficient of the camera (1x5)

    """
    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camMatrix,
                                                      distCoeff,
                                                      (w, h),
                                                      1,
                                                      (w, h)
                                                      )
    # undistort
    dst = cv2.undistort(img, camMatrix, distCoeff, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst


def main():
    calibrateCamera()

if __name__ == "__main__":
    main()
