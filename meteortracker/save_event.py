"""
@author(s): Nathan Heidt, Jean Nassar

In charge of saving meteor events to either a remote server or on the local
machine for debugging or future uploading.

It will upload to local and/or remote databases depending on what is specified
in the config.ini file.

"""
import configparser
import datetime
import numbers
import sqlite3
import sys

import cv2
import os

def _read(variable):
    return getattr(sys.modules[__name__], variable)


class EventLogger(object):
    """
    When a new event is detected, it is passed to this class to log it in 
    a sqlite database.

    Parameters
    ----------
    config_path : string
        This contains the path to the config file relative to this file

    Attributes
    ----------
    config : ConfigParser
        This is used to access and parse the data in the config file
    local_db_name : str
        This is the full path of the local sqlite database
    local_db_table_name : str
        The name of the table within the database to store new events
    remote_db_name : str
        A url pointing to the remote server
    local_image_location : str
        Images are stored in this directory, and the database points to them
    use_local : bool
        Specifies whether or not to store events locally
    use_remote : bool
        Specifies whether or not to send events to the remote database
    conn : sqlite3.Connection
        An instance of the connection to the local database used to access
        for storage
    """
    def __init__(self, config_path='config.ini'):
        config_path = os.path.abspath(os.path.join(
                                        os.path.dirname(__file__), config_path
                                        )
                                     )

        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        #get working variables from config file
        self.local_db_name = self.config['Database']['Local']
        self.local_db_table_name = self.config['Database']['LocalTable']
        self.remote_db_name = self.config['Database']['Remote']
        self.local_image_location = self.config['Database']['LocalImages']

        self.use_local = bool(self.config['Database']['UseLocal'])
        self.use_remote = bool(self.config['Database']['UseRemote'])

        self.conn = sqlite3.connect(self.local_db_name)

        #these are the names of the columns in the database
        self._variables = [('current_image',          'TEXT'),
                           ('previous_image',         'TEXT'), 
                           ('date',                   'TEXT'),
                           ('latitude',               'REAL'),
                           ('longitude',              'REAL'),
                           ('bearing',                'REAL'),
                           ('roll',                   'REAL'),
                           ('pitch',                  'REAL'),
                           ('yaw',                    'REAL'),
                           ('intrinsic_matrix',       'TEXT'), 
                           ('distortion_coefficient', 'TEXT')]
        # connect to db and create tables if they don't exist
        self._check_local_db()

    def __del__(self):
        """
        When this class is deleted (i.e. the program is killed) we want to
        ensure we gracefully close the connection to the database

        """
        self.conn.close()

    def add_event(self, current_image, previous_image):
        """
        When we detect a new event, it is passed to this function for storage

        Parameters
        ----------
        current_image : cv2.Image
            The current image of the detection event
        previous_image : cv2.Image
            The previous image of the detection event
        """
        date = datetime.datetime.utcnow().isoformat()
        latitude = self.config['Location']['Latitude']
        longitude = self.config['Location']['Longitude']
        bearing = self.config['Location']['Bearing']
        roll = self.config['Location']['Roll']
        pitch = self.config['Location']['Pitch']
        yaw = self.config['Location']['Yaw']

        intrinsic_matrix = "'" + self.config['Camera']['IntrinsicMat'] + "'"
        distortion_coefficient = "'" + \
                            self.config['Camera']['DistortionCoeff'] + "'"

        if self.use_local:
            self._upload_to_local(
                current_image, previous_image, date, latitude, longitude,
                bearing, roll, pitch, yaw,
                intrinsic_matrix, distortion_coefficient
            )
        if self.use_remote:
            self._upload_to_remote(
                current_image, previous_image, date, latitude, longitude,
                bearing, roll, pitch, yaw,
                intrinsic_matrix, distortion_coefficient
            )

    def _upload_to_remote(self, current_image, previous_image, date,
                         latitude, longitude, bearing,
                         roll, pitch, yaw,
                         intrinsic_matrix, distortion_coefficient):
        ...

    def _upload_to_local(self, current_image, previous_image, date,
                        latitude, longitude, bearing,
                        roll, pitch, yaw,
                        intrinsic_matrix, distortion_coefficient):
        """
        This takes all the parameters needed to upload an event to the 
        remote database

        Parameters
        ----------
        current_image : cv2.Image
            The current image from the detection event
        previous_image : cv2.Image
            The previous image from the detection event
        date : datetime
            The date and time the event occured
        latitude : float
            The geographical latitude of the camera
        longitude : float
            The geographical longitude of the camera
        bearing : float
            If there were an arrow starting from the middle of the camera
            and pointing down, this is the compass direction it is facing
        roll : float
            Rotation along the axis of the direction the camera is facing
        pitch : float
            Rotation along the side to side axis of the camera
        yaw : float
            Rotation along the vertical axis of the camera
        intrinsic_matrix : str
            A string containing the intrinsic matrix of the camera used for
            camera calibration, and angle calcuation
        distortion_coefficient : str
            A string containing the distortion coefficient used to remove 
            lensing in a camera image (like that in fisheye lenses)
        """
        # save the images locally, we don't want them in the database so they're
        # easier to work with
        filename_format = '{location}_{date}_{{order}}.jpg'.format(
            location=self.local_image_location, date=date)

        filename_current = filename_format.format(order='current')
        filename_previous = filename_format.format(order='previous')

        cv2.imwrite(filename_current, current_image)
        cv2.imwrite(filename_previous, previous_image)

        # This is more verbose than using locals() to index available
        # variables, but far less confusing
        values_to_add = [
            repr(filename_current),
            repr(filename_previous),
            repr(date),
            latitude,
            longitude,
            bearing,
            roll,
            pitch,
            yaw, 
            repr(intrinsic_matrix), 
            repr(distortion_coefficient)
        ]

        sql_template = 'insert into {table_name} ({fields}) values ({values})'
        db_command = sql_template.format(
            table_name=self.local_db_table_name,
            fields=", ".join(variable for (variable, _) in self._variables),
            values=", ".join(
                value
                for value in values_to_add
            )
        )

        self.conn.execute(db_command)
        self.conn.commit()

    def _check_local_db(self):
        """
        This ensures that the database exists and that the specified
        table exists within it.

        """
        sql_template = 'create table if not exists {table_name} ({fields})'
        db_command = sql_template.format(
            table_name = self.local_db_table_name,
            fields=", ".join(
                variable + " " + data_type
                for (variable, data_type) in self._variables
            )
        )
        c = self.conn.cursor()
        c.execute(db_command)
        self.conn.commit()


if __name__ == "__main__":
    print("starting in test mode")
    e = EventLogger()

