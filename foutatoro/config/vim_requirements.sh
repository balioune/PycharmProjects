#!/usr/bin/env bash

sudo apt-get update

sudo apt-get install python-pip python-dev libmysqlclient-dev -y

sudo pip install MySQL-python


sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password airbusds'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password airbusds'
sudo apt-get -y install mysql-server -y

mysql -uroot -p$MYSQL_PWD -e "CREATE DATABASE vim_db;"
