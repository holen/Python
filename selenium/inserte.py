#!/usr/bin/env python3
#coding: utf-8

import sys
import datetime
import pymongo

connection = pymongo.Connection('localhost', 27017)
db = connection.emaildb
qqtable = db.qq
data = '''{
        "email" : "%s",
        "name" : "%s",
        "sex" : "%s",
        "age" : %s,
        "place" : "%s",
        "status" : "None"
        }
    '''

data_list = []
data_list.append(data % (email, name, sex, age, place))
qqtable.insert(data_list)
