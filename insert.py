# -*- coding: utf-8 -*-
# @Author: Hu Wei
# @Email: hustwei@qq.com
# @DateTime: 2017-12-08 18:32:05
# @Last Modified by: Huwei
# @Last Modified time: 2017-12-11 18:56:52

import pymysql.cursors
import datetime
import random
import time
from config import dbconfig

insertsql = 'INSERT INTO iotform (CurrentTime, Tem1, Tem2, Tem3, Hum1, Hum2, Pre1, Pre2, LED1, LED2, LED3) \
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

def insert():
	connection = pymysql.connect(**dbconfig)
	with connection.cursor() as cursor:	
		while 1:
			args = (
				datetime.datetime.now(), 
				random.uniform(-10.0,40.0), 
				random.uniform(-10.0,40.0),
				random.uniform(-10.0,40.0),
				random.uniform(0,100), 
				random.uniform(0,100), 
				random.uniform(100,300), 
				random.uniform(100,300), 
				1,
				1,
				1,
			)
			cursor.execute(insertsql, args)
			time.sleep(1)
			connection.commit()
			print('insert', args)
	connection.close()
insert()