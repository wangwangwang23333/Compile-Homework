# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:09:34 2021

@author: 12094
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QStandardItem,QStandardItemModel
from PyQt5.QtCore import QSize
from PyQt5.Qt import *

class MainForm(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        '''
        窗体基本信息
        '''
        self.resize(1200,800)
        self.setWindowTitle('编译原理大作业——模块3：自下而上的语法分析')
        
        #窗口居中
        qr=self.frameGeometry()
        centerPlace=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerPlace)
        self.move(qr.topLeft())
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    mainForm=MainForm()
    mainForm.show()
    
    sys.exit(app.exec_())