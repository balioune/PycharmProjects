#!/bin/bash

# install Mysql server

sudo apt-get update

MYSQL_USER="airbusds"
MYSQL_PWD="airbusds"
MYSQL_CONNECT="mysql -uroot -p$MYSQL_PWD -e"

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password airbusds'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password airbusds'
sudo apt-get -y install mysql-server -y

mysql -uroot -p$MYSQL_PWD -e "CREATE DATABASE vim_db;"

mysql -uroot -p$MYSQL_PWD -e "CREATE USER 'airbusds'@'localhost' IDENTIFIED BY 'airbusds';"
mysql -uroot -p$MYSQL_PWD -e "GRANT ALL PRIVILEGES ON *.* TO 'airbusds'@'localhost' IDENTIFIED BY 'airbusds';"
mysql -uroot -p$MYSQL_PWD -e "GRANT ALL PRIVILEGES ON *.* TO 'airbusds'@'%' IDENTIFIED BY 'airbusds';"
mysql -uroot -p$MYSQL_PWD -e  "FLUSH PRIVILEGES;"





