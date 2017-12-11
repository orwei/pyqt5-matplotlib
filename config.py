# -*- coding: utf-8 -*-
# @Author: Hu Wei
# @Email: hustwei@qq.com
# @DateTime: 2017-12-09 15:39:07
# @Last Modified by: Huwei
# @Last Modified time: 2017-12-11 18:55:28

# 数据库配置
dbconfig = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'design',
}

# 线条1的格式
kwline1 = {
	'color':'blue', 
	'linestyle':'-', 
	'linewidth':1,
	'marker':None, 
	# 'markerfacecolor':'red', 
	# 'markeredgecolor':'black',
	# 'markeredgewidth':3, 
	# 'markersize':12
}

# 线条2的格式
kwline2 = {
	'color':'red',
	'linestyle':'-',
	'marker':None,
}

# 线条三的格式
kwline3 = {
	'color':'green',
	'linestyle':'-',
	'marker':None,
}

# 温度坐标系参数
TEMPERATURE = {
	'linenum':3,
	'linelabel1':'tem1',
	'linelabel2':'tem2',
	'linelabel3':'tem3',
	'ylim_min':-10,
	'ylim_max':40,
	'fieldname1':'Tem1',
	'fieldname2':'Tem2',
	'fieldname3':'Tem3',
	'ylabel':'Values of Temperature',
}

# 湿度坐标系参数
HUMIDITY = {
	'linenum':2,
	'linelabel1':'hum1',
	'linelabel2':'hum2',
	'ylim_min':0,
	'ylim_max':100,
	'fieldname1':'Hum1',
	'fieldname2':'Hum2',
	'ylabel':'Values of Humidity',
}

# 压强坐标系参数
PRESSURE = {
	'linenum':2,
	'linelabel1':'pre1',
	'linelabel2':'pre2',
	'ylim_min':100,
	'ylim_max':300,
	'fieldname1':'Pre1',
	'fieldname2':'Pre2',
	'ylabel':'Values of Prressure',
}
