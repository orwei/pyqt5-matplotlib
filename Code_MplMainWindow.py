# -*- coding: utf-8 -*-
# @Author: Hu Wei
# @Email: hustwei@qq.com
# @DateTime: 2017-12-07 20:40:27
# @Last Modified by: Huwei
# @Last Modified time: 2017-12-11 18:44:37

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication
from Ui_MplMainWindow import Ui_MainWindow
from config import TEMPERATURE, HUMIDITY, PRESSURE


class Code_MainWindow(Ui_MainWindow):
	def __init__(self, parent=None):
		super(Code_MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.temStartBtn.clicked.connect(self.temStartPlot)
		self.temPauseBtn.clicked.connect(self.temPausePlot)
		self.humStartBtn.clicked.connect(self.humStartPlot)
		self.humPauseBtn.clicked.connect(self.humPausePlot)
		self.preStartBtn.clicked.connect(self.preStartPlot)
		self.prePauseBtn.clicked.connect(self.prePausePlot)

	def temStartPlot(self):
		self.temwidget.startPlot(**TEMPERATURE)

	def temPausePlot(self):
		self.temwidget.pausePlot()

	def humStartPlot(self):
		self.humwidget.startPlot(**HUMIDITY)

	def humPausePlot(self):
		self.humwidget.pausePlot()

	def preStartPlot(self):
		self.prewidget.startPlot(**PRESSURE)

	def prePausePlot(self):
		self.prewidget.pausePlot()

	def releasePlot(self):
		self.humwidget.releasePlot()
		self.temwidget.releasePlot()
		self.prewidget.releasePlot()

	# 关闭事件？
	def closeEvent(self, event):
		result = QMessageBox.question(self,
				"退出",
				"确定退出？",
				QMessageBox.Yes | QMessageBox.No
			)	
		event.ignore()
		if result == QMessageBox.Yes:
			self.releasePlot()
			event.accept()

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	ui = Code_MainWindow()
	ui.show()
	sys.exit(app.exec_())