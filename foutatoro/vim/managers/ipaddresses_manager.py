#!/usr/bin/env python
# Author: Alioune BA

import MySQLdb
import uuid

class IpaddressesManager:

    def __init__(self, host, user,password, database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database


    def create_ipaddress (self, name, type):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "INSERT INTO IMAGES(ID, NAME, TYPE) \
               VALUES ('%s', '%s', '%s')" % \
              (uuid.uuid4(), name, type)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            print ("The image %s is registered" %(name))
            # Commit your changes in the database
            db.commit()
        except MySQLdb.Warning, e:
            print "I/O error({0}): {1}".format(e.message, e.args)
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

    def delete_ipaddress (self,id):
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


    def get_ipaddress (self,id):
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
                response.append(row[0])
                response.append(row[1])
                response.append(row[2])

            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

        return response


ip = IpaddressesManager("192.168.122.31",'airbusds','airbusds','vim_db')
ip.delete_image("0679453c-09c3-4560-bcb7-a7124af12673")
ip.delete_image("9e2701ee-2391-4b08-b9f7-f681be6c7797")
