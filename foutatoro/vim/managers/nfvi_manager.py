#!/usr/bin/env python
# Author: Alioune BA

import MySQLdb
from foutatoro.model.nfvi import Nfvi

class NfviManager:

    def __init__(self, host, user,password, database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database


    def create_nfvi (self,nfvi):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        print ('Creating NFVI %s, %s, %d,%d, %d' %(nfvi.get_id(), nfvi.get_hostname(), nfvi.get_cpu(), nfvi.get_ram(), nfvi.get_disk()))
        cursor = db.cursor()
        sql = "INSERT INTO NFVI(ID, NAME, CPU, RAM, DISK) \
               VALUES ('%s', '%s', '%d','%d', '%d')" % \
              (nfvi.get_id(), nfvi.get_hostname(), nfvi.get_cpu(), nfvi.get_ram(), nfvi.get_disk())
        try:
            # Execute the SQL command
            cursor.execute(sql)
            print ("The NFVI %s is registered" %(nfvi.get_id()))
            # Commit your changes in the database
            db.commit()
        except MySQLdb.Error, e:
            print "I/O error({0}): {1}".format(e.message, e.args)
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

    def delete_nfvi (self,id):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "DELETE FROM NFVI WHERE ID='%s'" %(id)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            print ("The NFVI with ID %s is removed" %(id))
            # Commit your changes in the database
            db.commit()
        except MySQLdb.Error, e:
            print "I/O error({0}): {1}".format(e.message, e.args)
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()


    def get_nfvi (self,id):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "SELECT * FROM NFVI WHERE ID='%s'" %(id)
        response = []
        try:
            # Execute the SQL command
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                response.append(Nfvi(row[0], row[1], int(row[2]),int(row[3]), int(row[4])))

            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        return response

    def get_all_nfvi (self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "SELECT * FROM NFVI"
        response = []
        try:
            # Execute the SQL command
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                response.append(Nfvi(row[0], row[1], int(row[2]),int(row[3]), int(row[4])))

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
ID2='5d7cf9cf-dc99-468b-9b4a-60680f0bf055'

nfvi = NfviManager("192.168.122.31",'airbusds','airbusds','vim_db')
nfvi.create_nfvi(Nfvi(ID, 'airbushost', 55, 4562,555))
nfvi.create_nfvi(Nfvi(ID1, 'host1', 55, 4562,555))
nfvi.create_nfvi(Nfvi(ID2, 'host2', 55, 4562,555))
for i in nfvi.get_all_nfvi():
    print (i.get_id())