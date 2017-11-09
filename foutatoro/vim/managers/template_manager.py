#!/usr/bin/env python
# Author: Alioune BA

import MySQLdb
import uuid


from foutatoro.model.template import Template

class TemplateManager:

    def __init__(self, host, user,password, database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database


    def create_template (self, template):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "INSERT INTO TEMPLATES(ID, NAME, CPU, RAM, DISK) \
               VALUES ('%s', '%s', '%d', '%d', '%d')" % \
              (uuid.uuid4(), template.get_name(), template.get_cpu(), template.get_ram(), template.get_disk())
        try:
            # Execute the SQL command
            cursor.execute(sql)
            print ("The TEMPALTE %s is registered" %(template.get_name()))
            # Commit your changes in the database
            db.commit()
        except MySQLdb.Error, e:
            print "I/O error({0}): {1}".format(e.message, e.args)
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

    def delete_template (self,id):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "DELETE FROM TEMPLATES WHERE ID='%s'" %(id)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            print ("The TEMPLATE with ID %s is removed" %(id))
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()


    def get_template (self,name):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "SELECT * FROM TEMPLATES WHERE NAME='%s'" %(name)
        response = []
        try:
            # Execute the SQL command
            cursor.execute(sql)
            print ("Return information if the TEMPLATE with ID %s" %(name))
            results = cursor.fetchall()

            for row in results:
                response.append(Template(row[1], int(row[2]), int(row[3]), int(row[4])))

            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

        return response

template = TemplateManager("192.168.122.31",'airbusds','airbusds','vim_db')
"""
template.create_template(Template("medium", 2, 1024, 5))
template.create_template(Template("small", 1, 504, 2))
template.create_template(Template("large", 5, 5024, 55))
"""

for i in template.get_template('medium'):
    i.__str__()