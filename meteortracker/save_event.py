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
    def __init__(self, config_path='config.ini'):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), config_path))
        
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
        self.check_local_db()

    def __del__(self):
        self.conn.close()

    def add_event(self, current_image, previous_image):
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
            self.upload_to_local(
                current_image, previous_image, date, latitude, longitude,
                bearing, roll, pitch, yaw,
                intrinsic_matrix, distortion_coefficient
            )
        if self.use_remote:
            self.upload_to_remote(
                current_image, previous_image, date, latitude, longitude,
                bearing, roll, pitch, yaw,
                intrinsic_matrix, distortion_coefficient
            )

    def upload_to_remote(self, current_image, previous_image, date,
                         latitude, longitude, bearing,
                         roll, pitch, yaw,
                         intrinsic_matrix, distortion_coefficient):
        ...

    def upload_to_local(self, current_image, previous_image, date,
                        latitude, longitude, bearing,
                        roll, pitch, yaw,
                        intrinsic_matrix, distortion_coefficient):
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

    def check_local_db(self):
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

