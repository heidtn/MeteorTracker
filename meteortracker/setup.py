import configparser
import camera_calibration

"""
@author(s): Nathan Heidt, Jean Nassar

This initializes necessary directories and files.

"""

import os
import numpy as np

db_dir = 'database'
im_dir = 'database/images'


def initialize(config_path='config.ini'):
    """
    Initializes the user settings and folders.

    Parameters
    ----------
    config_path : str
        the path of the config.ini file relative to this file

    """
    config_path = os.path.abspath(
                        os.path.join(
                                os.path.dirname(__file__), config_path
                            )
                        )

    config = configparser.ConfigParser()
    config.read(config_path)

    print("Setting up directories")
    setup_directories(config)
    print("\n")

    print("User setup")
    get_user_settings(config)
    print("\n")

    print("Camera calibration")
    calibrate_camera(config)
    print("\n")

    print("Writing to config file")
    with open(config_path, 'w') as configfile:
        config.write(configfile)


def setup_directories(config):
    if not os.path.exists(db_dir):
        print("creating database directory")
        os.makedirs(db_dir)
    if not os.path.exists(im_dir):
        print("creating image directory")
        os.makedirs(im_dir)

    db_path = os.path.abspath(db_dir)
    im_path = os.path.abspath(im_dir)

    config['Database']['Local'] = db_path + '/local.db'
    config['Database']['LocalImages'] = im_path + '/'


def get_user_settings(config):
    setup = input("Would you like to answer the setup questions? (Y/n): ")
    if setup is not '' and setup.lower() is not 'y':
        print("Skipping setup")
        return

    print("\nFind the geographical coordinates of your location")

    latitude = _get_input_float(
                            "Enter your latitude with format nnn.nnnnnn: "
                               )
    longitude = _get_input_float(
                            "Enter your longitude with format nnn.nnnnnn: "
                                )

    print("\nDetermine the orientation of your camera."
          " It is best if the camera faces directly upwards.")

    roll = _get_input_float(
                            "Enter the roll angle of the camera in degrees: "
                           )
    pitch = _get_input_float(
                            "Enter the pitch angle of the camera in degrees: "
                            )
    yaw = _get_input_float(
                            "Enter the yaw angle of the camera in degrees: "
                          )

    print("\nTo get the bearing, if you took a picture with the camera, "
          "which compass direction would be down (0.0 being north 180.0 "
          "being south")

    bearing = _get_input_float(
                          "Enter the bearing angle of the camera in degrees: "
                              )

    config['Location']['latitude']
    config['Location']['longitude']
    config['Location']['roll']
    config['Location']['pitch']
    config['Location']['yaw']
    config['Location']['bearing']


def calibrate_camera(config):
    setup = input("Would you like to calibrate the camera? (Y/n): ")
    if setup is not '' and setup.lower() is not 'y':
        print("Skipping setup")
        return

    intrinsic_matrix, distortion_coeff = camera_calibration.calibrate_camera()

    string_matrix = str(intrinsic_matrix.reshape(9))[1:-1]
    string_distortion = str(distortion_coeff)[1:-1]

    config['Camera']['intrinsicmat'] = string_matrix
    config['Camera']['distortioncoeff'] = string_distortion


def _get_input_float(request):
    while True:
        value = input(request)
        try:
            value = float(latitude)
            return value
        except ValueError:
            print("Please make sure your entry has only numbers")


if __name__ == "__main__":
    initialize()
