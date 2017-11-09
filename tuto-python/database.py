#!/usr/bin/python
import MySQLdb
class Database:

    def __init__(self, host, user,password, database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database

    def connect_db(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print "Database version : %s " % data
        db.close()

    def create_table_employee(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
        sql = """CREATE TABLE EMPLOYEE (
                 FIRST_NAME  CHAR(20) NOT NULL,
                 LAST_NAME  CHAR(20),
                 AGE INT,  
                 SEX CHAR(1),
                 INCOME FLOAT )"""

        cursor.execute(sql)

        # disconnect from server
        db.close()

    def insert_static_values(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
                 LAST_NAME, AGE, SEX, INCOME)
                 VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        # disconnect from server
        db.close()

    def insert_dynamic_values(self,lastname,firstname,age,sex,income):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
               LAST_NAME, AGE, SEX, INCOME) \
               VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
              (lastname, firstname, age, sex, income)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        # disconnect from server
        db.close()

    def read_all_employee(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        sql = "SELECT * FROM EMPLOYEE \
               WHERE INCOME > '%d'" % (1000)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                fname = row[0]
                lname = row[1]
                age = row[2]
                sex = row[3]
                income = row[4]
                print "fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
              (fname, lname, age, sex, income)
        except:
            print "Error: unable to fecth data"
        db.close()

test = Database ("localhost","testuser","test123","TESTDB" )
test.connect_db()
test.create_table_employee()
test.insert_static_values()
test.insert_dynamic_values("alioune","ba",28,'M',60000)
test.read_all_employee()