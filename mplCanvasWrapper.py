# -*- coding: utf-8 -*-
# @Author: Hu Wei
# @Email: hustwei@qq.com
# @DateTime: 2017-12-07 20:57:32
# @Last Modified by: Huwei
# @Last Modified time: 2017-12-11 18:56:46


from PyQt5.QtWidgets import *

import matplotlib
matplotlib.use('Qt5Agg')  # 申明使用Qt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.dates import date2num, MinuteLocator, SecondLocator, DateLocator, DateFormatter
from matplotlib.figure import Figure

from datetime import datetime
import threading
import time
import pymysql.cursors

from config import kwline1, kwline2, kwline3, dbconfig

X_MINUTES = 1
INTERVAL = 1
MAXCOUNTER = int(X_MINUTES*60/INTERVAL)
# 通过继承FigureCanvas类，使得该类既是一个PyQt5的QWidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplot 
class MplCanvas(FigureCanvas):  
	def __init__(self):
		# 创建一个Figure，注意：该Figure为matplotlib下的.figure，不是matplotlib.pyplot下面的figure
		self.figure = Figure()	
		FigureCanvas.__init__(self, self.figure)  # 初始化父类
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.ax = self.figure.add_subplot(111)  # 创建一个新的 1 * 1 的子图，接下来的图样绘制在其中的第 1 块（也是唯一的一块）
		self.ax.set_xlabel('Time')	# 设置x坐标轴名
		self.ax.grid(True)  # 为坐标系设置网格
		self.ax.xaxis.set_major_locator(SecondLocator([0,20,40]))  # 主刻度，10s间隔
		self.ax.xaxis.set_minor_locator(SecondLocator([0,5,10,15,20,25,30,35,40,45,50,55])) # 次刻度，5s间隔
		self.ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S')) # x坐标主刻度名格式
		self.curveObj1 = None # draw object
		self.curveObj2 = None
		self.curveObj3 = None

	def plot2(self, datax, datay1, datay2, **plotname):  # 描点
		if (self.curveObj1 and self.curveObj2) is None :
			self.ax.set_ylabel(plotname['ylabel'])
			self.ax.set_ylim(plotname['ylim_min'], plotname['ylim_max'])  # 设置y轴上下限
			self.curveObj1 = self.ax.plot_date(datax, datay1, **kwline1, label=plotname['linelabel1'])[0]  # 画到时间序列图，plot_date()函数可以满足要求，kwline表示线条dict参数
			self.curveObj2 = self.ax.plot_date(datax, datay2, **kwline2, label=plotname['linelabel2'])[0]
			# print(numpy.array(datax), numpy.array(datay))
			# [ 736671.73638582] [46]
			# print(self.ax.plot_date(numpy.array(datax), numpy.array(datay), **lineargs))
			# [<matplotlib.lines.Line2D object at 0x0000017EAE465860>]
			# print(self.curveObj)
			# Line2D(Temperature)
			self.ax.legend(loc='upper left')  # 对图标的标注
		else:
			self.curveObj1.set_data(datax, datay1)
			self.curveObj2.set_data(datax, datay2)
			self.ax.set_xlim(datax[0], datax[-1])  # 设置x轴上下限	
		# ticklabels = self.ax.xaxis.get_ticklabels()
		# for tick in ticklabels:
		# 	tick.set_rotation(0) # 刻度文本旋转0度
		self.draw()

	def plot3(self, datax, datay1, datay2, datay3, **plotname):
		if (self.curveObj1 and self.curveObj2 and self.curveObj3) is None:
			self.ax.set_ylabel(plotname['ylabel'])
			self.ax.set_ylim(plotname['ylim_min'], plotname['ylim_max'])
			self.curveObj1 = self.ax.plot_date(datax, datay1, **kwline1, label=plotname['linelabel1'])[0]
			self.curveObj2 = self.ax.plot_date(datax, datay2, **kwline2, label=plotname['linelabel2'])[0]
			self.curveObj3 = self.ax.plot_date(datax, datay3, **kwline3, label=plotname['linelabel3'])[0]
			self.ax.legend(loc='upper left')  # 对图标的标注
		else:
			self.curveObj1.set_data(datax, datay1)
			self.curveObj2.set_data(datax, datay2)
			self.curveObj3.set_data(datax, datay3)
			self.ax.set_xlim(datax[0], datax[-1])
		self.draw()



class MplCanvasWrapper(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.canvas = MplCanvas()
		self.vboxlayout = QVBoxLayout()
		# self.navtoolbar = NavigationToolbar(self.canvas, parent)
		# self.vboxlayout.addWidget(self.navtoolbar)
		self.vboxlayout.addWidget(self.canvas)
		self.setLayout(self.vboxlayout)
		self.dataX = []
		self.dataY1 = []
		self.dataY2 = []
		self.dataY3 = []
		self.initDataGenerator()

	def startPlot(self, **plotname):
		self.__generating = True
		self.plotname = plotname
		pass

	def pausePlot(self):
		self.__generating = False	
		pass

	def initDataGenerator(self):
		self.__generating = False
		self.__exit = False
		self.tData = threading.Thread(name='dataGenerator', target=self.generateData)
		self.tData.start()  # 线程开始

	def releasePlot(self):
		self.__exit = True
		self.tData.join()	# 线程退出

	def generateData(self):
		counter = 0
		selectsql = 'SELECT * FROM iotform ORDER BY id DESC limit 1;'
		# selectsql = 'SELECT %s, %s FROM iotform ORDER BY CurrentTime DESC limit 1;' \
				# % (self.fieldname1, self.fieldname2)	
		while 1:
			if self.__exit:
				break

			if self.__generating and self.plotname['linenum'] == 3:
				conn3 = pymysql.connect(**dbconfig, cursorclass=pymysql.cursors.DictCursor)
				with conn3.cursor() as cursor:					
					cursor.execute(selectsql)
					row = cursor.fetchone()
					# print(row)
					self.dataY1.append(row[self.plotname['fieldname1']])
					self.dataY2.append(row[self.plotname['fieldname2']])
					self.dataY3.append(row[self.plotname['fieldname3']])
				conn3.close()			
				self.dataX.append(date2num(datetime.now()))	
				self.canvas.plot3(self.dataX, self.dataY1, self.dataY2, self.dataY3, **self.plotname)
				if counter >= MAXCOUNTER:
					self.dataX.pop(0)
					self.dataY1.pop(0)
					self.dataY2.pop(0)
					self.dataY3.pop(0)
				else:
					counter += 1

			if self.__generating and self.plotname['linenum'] == 2:
				conn2 = pymysql.connect(**dbconfig, cursorclass=pymysql.cursors.DictCursor)
				with conn2.cursor() as cursor:					
					cursor.execute(selectsql)
					row = cursor.fetchone()
					# print(row)
					self.dataY1.append(row[self.plotname['fieldname1']])
					self.dataY2.append(row[self.plotname['fieldname2']])
				conn2.close()			
				self.dataX.append(date2num(datetime.now()))	
				self.canvas.plot2(self.dataX, self.dataY1, self.dataY2, **self.plotname)
				if counter >= MAXCOUNTER:
					self.dataX.pop(0)
					self.dataY1.pop(0)
					self.dataY2.pop(0)
				else:
					counter += 1

			time.sleep(INTERVAL)  # 每秒更新一次
			