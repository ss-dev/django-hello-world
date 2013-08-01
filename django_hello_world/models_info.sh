#!/bin/bash

date=`date +%y-%m-%d`

../.env/bin/python ./manage.py models_info ../.env/bin 2> "$date.dat"