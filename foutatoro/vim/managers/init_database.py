#!/usr/bin/env python
# Author: Alioune BA

import MySQLdb

class InitDatabase:

    def __init__(self, host, user,password, database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database

    """ Connection to the database"""
    def connect_db(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print "Database version : %s " % data
        db.close()

    """ Creating tables """
    def create_table_nfvi(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS NFVI")
        sql = """CREATE TABLE NFVI (
                 ID  VARCHAR(36) PRIMARY KEY,
                 NAME  CHAR(20),
                 CPU INT,  
                 RAM INT, 
                 DISK INT)"""
        cursor.execute(sql)
        # disconnect from server
        db.close()

    def create_table_images(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS IMAGES")
        sql = """CREATE TABLE IMAGES (
                 ID  VARCHAR(36) NOT NULL PRIMARY KEY,
                 NAME  CHAR(60),
                 TYPE ENUM('DOCKER', 'KVM') NOT NULL,
                 NFVI  VARCHAR(36),
                 FOREIGN KEY (NFVI) REFERENCES NFVI(ID) ON DELETE CASCADE) """
        cursor.execute(sql)
        db.close()

    def create_table_networks(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        #cursor.execute("DROP TABLE IF EXISTS NETWORKS")
        sql = """CREATE TABLE NETWORKS (
                 ID  VARCHAR(36) NOT NULL,
                 NAME  CHAR(20),
                 ADDRESS  CHAR(15),
                 MASK  CHAR(15),
                 NFVI  VARCHAR(36),
                 TYPE ENUM('EXTERNAL', 'PRIVATE','MANAGEMENT'),
                 NIC  CHAR(15),
                 PRIMARY KEY (ID),
                 FOREIGN KEY (NFVI) REFERENCES NFVI(ID) ON DELETE CASCADE)"""
        cursor.execute(sql)
        db.close()

    def create_table_template(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS TEMPLATES")
        sql = """CREATE TABLE TEMPLATES (
                 ID  VARCHAR(36) NOT NULL PRIMARY KEY,
                 NAME  CHAR(20),
                 CPU INT,
                 RAM INT,
                 DISK INT)"""
        cursor.execute(sql)
        db.close()

    def create_table_ipaddress(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS IP_ADDRESSES")
        sql = """CREATE TABLE IP_ADDRESSES (
                 ID  VARCHAR(36) NOT NULL PRIMARY KEY,
                 NETWORK VARCHAR(36),
                 IP  CHAR(15) NOT NULL,
                 MASK  CHAR(15) DEFAULT '255.255.255.0',
                 FOREIGN KEY (NETWORK) REFERENCES NETWORKS(ID)
                 )"""
        cursor.execute(sql)
        db.close()

    def create_table_computes(self):
        db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        cursor = db.cursor()
        #cursor.execute("DROP TABLE IF EXISTS NETWORKS")
        sql = """CREATE TABLE COMPUTES (
                 ID  CHAR(36) NOT NULL PRIMARY KEY,
                 NAME  CHAR(20),
                 IMAGE VARCHAR(36),
                 NETWORK VARCHAR(36),
                 NFVI  VARCHAR(36),
                 TEMPLATE VARCHAR(36),
                 IP CHAR(36),
                 TYPE ENUM('DOCKER', 'KVM'),
                 FOREIGN KEY (NFVI) REFERENCES NFVI(ID),
                 FOREIGN KEY (NETWORK) REFERENCES NETWORKS(ID),
                 FOREIGN KEY (IMAGE) REFERENCES IMAGES(ID),
                 FOREIGN KEY (TEMPLATE) REFERENCES TEMPLATES(ID),
                 FOREIGN KEY (IP) REFERENCES IP_ADDRESSES(ID)
                 )"""
        cursor.execute(sql)
        db.close()


    def create_all_tables(self):
        self.create_table_nfvi()
        self.create_table_images()
        self.create_table_template()
        self.create_table_networks()
        self.create_table_ipaddress()
        self.create_table_computes()

db = InitDatabase("127.0.0.1",'airbusds','airbusds','vim_db')
db.create_all_tables()