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
from bottomTopAlgorithm.OperatorPrecedenceGrammar import OperatorPrecedenceGrammar
from bottomTopAlgorithm.LRk_state_transfer_generation import LR0,LR1


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
        self.tab2=WidgetUI2()
        self.tab4=WidgetUI4()
        
        # 加入顶层窗口
        self.addTab(self.tab1,"算法3.1")
        self.addTab(self.tab2,"算法3.2")
        self.addTab(self.tab4,"算法3.4")
        
 
class WidgetUI1(QWidget):
    def __init__(self):
        super().__init__()



        self.te = QTextEdit(self)
        self.te.move(50,200)
        self.te.setFontFamily("幼圆")
        self.te.setFontPointSize(20)
        label1=QLabel("输入文法规则",self)
        label1.move(50,170)


        self.outputArea = QTextEdit(self)
        self.outputArea.move(600,200)
        self.outputArea.setReadOnly(True)
        label2=QLabel("输出",self)
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


class WidgetUI2(QWidget):
    def __init__(self):
        super().__init__()

        self.te = QTextEdit()
        self.te.setPlaceholderText("在此输入文法规则")
        self.te.setFontFamily("幼圆")
        self.te.setFontPointSize(20)

        self.dealButton=QPushButton(self)
        self.dealButton.setText("生成优先关系表")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 10))
        self.dealButton.setToolTip("为算符优先文法生成算符之间的优先关系表")
        self.dealButton.resize(self.dealButton.sizeHint())
        self.dealButton.move(400,250)


        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 10))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())
        self.exampleButton.move(400,300)

        self.tableView=QTableView()
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.tableView.horizontalHeader().setStretchLastSection(True)
        

        layout=QVBoxLayout()
        layout.addWidget(self.tableView)
        layout.addWidget(self.te)
        layout.addWidget(self.dealButton)
        layout.addWidget(self.exampleButton)
        self.setLayout(layout)
  
    def calculate(self):
        try:


            opg = OperatorPrecedenceGrammar()
            res = self.te.toPlainText().split("\n")
            opg.setGrammar(res)
            opg.getPriorityTable()
            vnLen = len(opg.grammarManager.VT)

            # 建立vnLen * vnLen 的表格
            self.model=QStandardItemModel(vnLen,vnLen)
            # 设置水平方向头标签文本内容
            self.model.setHorizontalHeaderLabels(opg.grammarManager.VT)
            # 设置竖直方向
            self.model.setVerticalHeaderLabels(opg.grammarManager.VT)
         
            for row in range(vnLen):
                for column in range(vnLen):
                    if (opg.grammarManager.VT[row],
                    opg.grammarManager.VT[column]) in opg.priorityTable:
                        item=QStandardItem(opg.priorityTable[(opg.grammarManager.VT[row],
                    opg.grammarManager.VT[column])])
                    else:
                        item=QStandardItem(' ')
                    self.model.setItem(row,column,item)
            
            
            self.tableView.setModel(self.model)
            
        except:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("输入有误，请检查您的输入！")
            errorMessage.exec_()

    def getExample(self):
        self.te.setText("S→a│^│(T)\nT→T,S│S")
    
class WidgetUI4(QWidget):
    def __init__(self):
        super().__init__()

        
        # 文法选择按钮
        self.rb1 = QRadioButton('LR(0)文法')
        self.rb1.setChecked(True)
        self.rb2 = QRadioButton('LR(1)文法')
        self.buttonGroup=QButtonGroup()
        self.buttonGroup.addButton(self.rb1,1)
        self.buttonGroup.addButton(self.rb2,2)
        

        # 文法输入框
        self.te = QTextEdit()
        self.te.setPlaceholderText("在此输入文法规则")
        self.te.setFontFamily("幼圆")
        self.te.setFontPointSize(20)

        vLayout1=QVBoxLayout()
        vLayout1.addWidget(self.rb1)
        vLayout1.addWidget(self.rb2)
        vLayout1.addWidget(self.te)

        # 水平方向
        hLayout1=QHBoxLayout()

  
        # 展示表格
        self.tableView=QTableView()
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        
        # 展示图片
        self.imageLabel = QLabel()
        self.imageLabel.setText(" ")
        self.imageLabel.setFixedHeight(500)
        self.g=None

        vLayout1.addWidget(self.tableView)
        
        hLayout1.addLayout(vLayout1)
        hLayout1.addWidget(self.imageLabel)

        vLayout2=QHBoxLayout()
        # 计算按钮
        self.dealButton=QPushButton(self)
        self.dealButton.setText("生成状态转移矩阵/DFA图")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.dealButton.setToolTip("为上下文无关文法构造识别文法活前缀的 DFA")
        self.dealButton.resize(self.dealButton.sizeHint())
        # 范例按钮
        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())
        # 保存图片
        self.saveButton=QPushButton(self)
        self.saveButton.setText("保存图片")
        self.saveButton.clicked.connect(self.saveImage)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.saveButton.setToolTip("您可以保存生成的DFA图")
        self.saveButton.resize(self.saveButton.sizeHint())
        

        vLayout2.addWidget(self.dealButton)
        vLayout2.addWidget(self.exampleButton)
        vLayout2.addWidget(self.saveButton)

        hLayout2=QVBoxLayout()
        hLayout2.addLayout(hLayout1)
        hLayout2.addLayout(vLayout2)


        
        self.setLayout(hLayout2)

    def getExample(self):
        try:
            self.model.clear()
        except:
            pass
        if self.rb1.isChecked():
            self.te.setText("E' → E\nE->(E)\nE->i")
        else:
            self.te.setText("S'->S\nS->BB\nB->aB\nB->b")

    def calculate(self):
        try:
            res = self.te.toPlainText().split("\n")
            
            if self.rb1.isChecked():
                lr0 = LR0()
            else:
                lr0=LR1()
            lr0.setGrammar(res)
            lr0.calculateDFA()
            print(lr0.translationArray)

            transCondition=lr0.grammarManager.VT+lr0.grammarManager.VN
            print("test",transCondition)
            transCondition.remove(lr0.grammarManager.sentences[0][0])
            
            print(transCondition)

            # 建立表格
            self.model=QStandardItemModel(len(lr0.states),len(transCondition))
            self.model.setHorizontalHeaderLabels(transCondition)
            self.model.setVerticalHeaderLabels([str(i) for i in range(len(lr0.states))])

            for row in range(len(lr0.states)):
                for column in range(len(transCondition)):
                    if ((row,transCondition[column])) in lr0.translationArray:
                        item=QStandardItem(str(lr0.translationArray[(row,transCondition[column])]))
                    else:
                        item=QStandardItem(' ')
                    self.model.setItem(row,column,item)
            
            baseUrl,self.g=lr0.getImage()
            baseUrl="outputImage//"+baseUrl
            self.g.render(baseUrl)
            self.imgUrl=baseUrl+".png"
            self.tableView.setModel(self.model)
            
            print(self.imgUrl)
            # 加载图片
            DFAImage = QPixmap(self.imgUrl).scaledToHeight(500)
            self.imageLabel.setPixmap(DFAImage)
            
            
        except error:
            print(error)
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("输入有误，请检查您的输入！")
            errorMessage.exec_()


    def saveImage(self):
        if self.g==None:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("请先生成DFA图！")
            errorMessage.exec_()
            return
        self.g.view()


if __name__=='__main__':
    app=QApplication(sys.argv)
    mainForm=MainForm()
    mainForm.show()
    
    sys.exit(app.exec_())