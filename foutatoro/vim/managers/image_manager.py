#!/usr/bin/env python
# Author: Alioune BA

import MySQLdb
import uuid

from foutatoro.model.image import Image

class ImageManager:

    def __init__(self, host, user,password, database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database


    def create_image (self, image):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "INSERT INTO IMAGES(ID, NAME, TYPE, NFVI) \
               VALUES ('%s', '%s', '%s', '%s')" % \
              (uuid.uuid4(), image.get_name(), image.get_type(), image.get_nfvi())
        try:
            # Execute the SQL command
            cursor.execute(sql)
            print ("The image %s is registered" %(image.get_name()))
            # Commit your changes in the database
            db.commit()
        except MySQLdb.Warning, e:
            print "I/O error({0}): {1}".format(e.message, e.args)
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

    def delete_image (self,id):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "DELETE FROM IMAGES WHERE ID='%s'" %(id)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            print ("The image with ID %s is removed" %(id))
            # Commit your changes in the database
            db.commit()
        except MySQLdb.Warning, e:
            print "I/O error({0}): {1}".format(e.message, e.args)
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()


    def get_image (self,id):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "SELECT * FROM IMAGES WHERE ID='%s'" %(id)
        response = []
        try:
            # Execute the SQL command
            cursor.execute(sql)
            print ("Return information if the image with ID %s" %(id))
            results = cursor.fetchall()

            for row in results:
                response.append(Image(row[1], row[2], row[3]))

            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

        return response


    def get_all_image (self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "SELECT * FROM IMAGES"
        response = []
        try:
            # Execute the SQL command
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                response.append(Image(row[1], row[2], row[3]))

            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

        return response

ID='dd7cf9cf-dc99-468b-9b4a-60680f0bf05c'
ID1='dd7cf9cf-dc99-468b-9b4a-60680f0bf055'
ID2='5d7cf9cf-dc99-468b-9b4a-60680f011f055'
image = ImageManager("192.168.122.31",'airbusds','airbusds','vim_db')
image.create_image(Image("ubuntu14", "DOCKER", ID2))

for i in image.get_all_image():
    print (i.get_name())
