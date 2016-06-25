import configparser
"""
@author(s): Nathan Heidt, Jean Nassar

This initializes necessary directories and files.

"""

import os

db_dir = 'Database'
im_dir = 'Database/images'


def initialize(config_path='config.ini'):
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

    config.set('Database', 'Local', db_path + '/local.db')
    config.set('Database', 'LocalImages', im_path + '/')

    with open(config_path, 'wb') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    initialize()
