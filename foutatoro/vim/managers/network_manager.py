#!/usr/bin/env python
# Author: Alioune BA

import MySQLdb
import uuid

from foutatoro.model.network import NetworkType
from foutatoro.model.network import Network

class NetworkManager:

    def __init__(self, host, user,password, database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database


    def add_network (self, name, address, mask, type, nfvi):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()

        sql = "INSERT INTO NETWORKS(ID, NAME, ADDRESS, MASK, NFVI, TYPE) \
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
              (uuid.uuid4(),name, address,mask,nfvi, type)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
            print ("Network %s is created" % (name))
        except MySQLdb.Error, e:
            print "I/O error({0}): {1}".format(e.message, e.args)
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

    def delete_network (self,id):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "DELETE FROM NETWORKS WHERE ID='%s'" %(id)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
            print ("The network with ID %s is removed" %(id))
        except MySQLdb.Error, e:
            print "I/O error({0}): {1}".format(e.message, e.args)
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

    def get_network (self,id):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "SELECT * FROM NETWORKS WHERE ID='%s'" %(id)
        response = []
        try:
            # Execute the SQL command
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                response.append(Network(row[1], row[2], row[5],row[6],row[3], row[4]))
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        return response

    def get_all_networks (self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "SELECT * FROM NETWORKS"
        response = []
        try:
            # Execute the SQL command
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                response.append(Network(row[1], row[2], row[5], row[6], row[3], row[4]))

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

net = NetworkManager("192.168.122.31",'airbusds','airbusds','vim_db')

#net.delete_network('')

net.add_network('net2','192.168.2.0','255.255.255.0','MANAGEMENT', ID)
net.add_network('net1','192.168.1.0','255.255.255.0','PRIVATE', ID1)


for i in net.get_all_networks():
    print (i.get_name())
