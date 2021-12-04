# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:09:34 2021

@author: 12094
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QStandardItem,QStandardItemModel
from PyQt5 import QtCore
from PyQt5.Qt import *
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

from bottomTopAlgorithm.GrammarManager import GrammarManager

class MainForm(QTabWidget):
    
    def __init__(self):
        super().__init__()
        
        '''
        窗体基本信息
        '''
        self.resize(900,600)
        self.setWindowTitle('编译原理大作业——模块3：自下而上的语法分析')
        self.setWindowIcon(QIcon('assets/icon.ico'))

        #窗口居中
        qr=self.frameGeometry()
        centerPlace=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerPlace)
        self.move(qr.topLeft())
        
        # 选项卡控件
        self.tab1=WidgetUI1()
        
        
        # 加入顶层窗口
        self.addTab(self.tab1,"算法3.1")
        
 
class WidgetUI1(QWidget):
    def __init__(self):
        super().__init__()



        self.te = QTextEdit(self)
        self.te.move(50,200)
        label1=QLabel("输入文法规则",self)
        label1.move(50,170)


        self.outputArea = QTextEdit(self)
        self.outputArea.move(600,200)
        self.outputArea.setReadOnly(True)
        label2=QLabel("输入文法规则",self)
        label2.move(600,170)

        self.dealButton=QPushButton(self)
        self.dealButton.setText("计算FirstVT和LastVT")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 10))
        self.dealButton.setToolTip("为非终结符生成 FIRSTVT/LASTVT 集合\n输入：文法产生式\n输出：文法符号的 FIRSTVT 和 LASTVT 集合内容")
        self.dealButton.resize(self.dealButton.sizeHint())
        self.dealButton.move(400,250)


        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 10))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())
        self.exampleButton.move(400,300)

    
    
    def calculate(self):
        self.outputArea.clear()
        try:
            g=GrammarManager()
        
            res=self.te.toPlainText().split("\n")
            g.getStr(res)

            g.getFirstAndLastVT()
            self.outputArea.setText("FirstVT:\n"+str(g.FIRSTVT)+"\nLastVT:\n"+str(g.LASTVT))
            print("res",res)
        except:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("输入有误，请检查您的输入！")
            errorMessage.exec_()
        
        return

    def getExample(self):
        self.te.setText("S→a│^│(T)\nT→T,S│S")

if __name__=='__main__':
    app=QApplication(sys.argv)
    mainForm=MainForm()
    mainForm.show()
    
    sys.exit(app.exec_())