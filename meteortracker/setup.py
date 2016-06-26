import configparser

"""
@author(s): Nathan Heidt, Jean Nassar

This initializes necessary directories and files.

"""

import os

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

    print("writing to config file")
    with open(config_path, 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    initialize()
