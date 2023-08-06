#!/bin/bash

service mysql start

sleep 5

# Check if the database exists and if not create it
echo "SHOW SCHEMAS;" | mysql | grep "{{ database }}"
ret=$?
if [ $ret -ne 0 ];
then
  echo "CREATE DATABASE {{ database }}" | mysql
fi

# Check if the user exists and if not create it
echo "SELECT user FROM mysql.user;" | mysql | grep "{{ username }}"
ret=$?
if [ $ret -ne 0 ];
then
  echo "CREATE USER {{ username }} IDENTIFIED BY '{{ password }}';" | mysql
fi

# Grant the user all privileges to the database
echo "GRANT ALL PRIVILEGES ON {{ database }}.* TO {{ username }};" | mysql

service mysql stop
