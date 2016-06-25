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


def _read(variable):
    return getattr(sys.modules[__name__], variable)


class EventLogger(object):
    def __init__(self, config_path='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        #get working variables from config file
        self.local_db_name = self.config.get('Database', 'Local', 0)
        self.local_db_table_name = self.config.get('Database', 'LocalTable', 0)
        self.remote_db_name = self.config.get('Database', 'Remote', 0)
        self.local_image_location = self.config.get('Database',
                                                    'LocalImages',
                                                    0)

        self.use_local = bool(self.config.get('Database', 'UseLocal', 0))
        self.use_remote = bool(self.config.get('Database', 'UseRemote', 0))

        self.conn = sqlite3.connect(self.local_db_name)
        # connect to db and create tables if they don't exist
        self.check_local_db()

        self._variables = ['current_image', 'previous_image', 'date',
                           'latitude', 'longitude', 'bearing',
                           'roll', 'pitch', 'yaw',
                           'intrinsic_matrix', 'distortion_coefficient']

    def __del__(self):
        self.conn.close()

    def add_event(self, current_image, previous_image):
        date = datetime.datetime.utcnow().isoformat()
        latitude = self.config.get('Location', 'Latitude', 0)
        longitude = self.config.get('Location', 'Longitude', 0)
        bearing = self.config.get('Location', 'Bearing', 0)
        roll = self.config.get('Location', 'Roll', 0)
        pitch = self.config.get('Location', 'Pitch', 0)
        yaw = self.config.get('Location', 'Yaw', 0)

        intrinsic_matrix = self.config.get('Camera', 'IntrinsicMat', 0)
        distortion_coefficient = self.config.get('Camera', 'DistortionCoeff', 0)

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

        sql_template = 'insert into {table_name} ({fields}) values ({values})'
        db_command = sql_template.format(
            table_name=self.local_db_table_name,
            fields=", ".join(variables),
            values=", ".join(str(_read(variable))
                             for variable in self._variables)
        )
        self.conn.execute(db_command)
        self.conn.commit()

    def check_local_db(self):
        sql_template = 'create table if not exists {table_name} ({fields})'
        db_command = sql_template.format(
            table_name = self.local_db_table_name,
            fields=", ".join(
                variable
                + (" REAL" if isinstance(_read(variable), numbers.Real) else "")
                for variable in self._variables
            )
        )
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()


if __name__ == "__main__":
    print("starting in test mode")
    e = EventLogger()

