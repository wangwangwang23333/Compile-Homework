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
from bottomTopAlgorithm.LR0_analysis_table import LR0Table
from bottomTopAlgorithm.LR1_analysis_table import LR1Table
from bottomTopAlgorithm.LALR_analysis_table import LALRTable
from bottomTopAlgorithm.stack import Stack

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
        self.tab3=WidgetUI3()
        self.tab4=WidgetUI4()
        self.tab5=WidgetUI5()
        self.tab6=WidgetUI6()
        self.tab7=WidgetUI7()
        self.tab8=WidgetUI8()
        self.tab9=WidgetUI9()
        self.tab10=ComprehensiveExperiment()
        
        # 加入顶层窗口
        self.addTab(self.tab1,"算法3.1")
        self.addTab(self.tab2,"算法3.2")
        self.addTab(self.tab3,"算法3.3")
        self.addTab(self.tab4,"算法3.4")
        self.addTab(self.tab5,"算法3.5")
        self.addTab(self.tab6,"算法3.6")
        self.addTab(self.tab7,"算法3.7")
        self.addTab(self.tab8,"算法3.8")
        self.addTab(self.tab9,"算法3.9")

        self.addTab(self.tab10,"综合实验")
        
 
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
            
            
        except:
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

class WidgetUI3(QWidget):
    def __init__(self):
        super().__init__()

class WidgetUI5(QWidget):
    def __init__(self):
        super().__init__()

        # 文法输入框
        self.te = QTextEdit()
        self.te.setPlaceholderText("在此输入文法规则")
        self.te.setFontFamily("幼圆")
        self.te.setFontPointSize(20)

        # 计算按钮
        self.dealButton=QPushButton(self)
        self.dealButton.setText("构造LR(0)分析表")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.dealButton.setToolTip("根据识别文法活前缀的 DFA 构造 LR(0)分析表")
        self.dealButton.resize(self.dealButton.sizeHint())
        # 范例按钮
        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())

        vLayout=QVBoxLayout()
        vLayout.addWidget(self.te)
        vLayout.addWidget(self.dealButton)
        vLayout.addWidget(self.exampleButton)
   
        hLayout=QHBoxLayout()
        hLayout.addLayout(vLayout)

        # 表格1
        actionVLayout=QVBoxLayout()
        actionLabel=QLabel()
        actionLabel.setAlignment(Qt.AlignCenter)
        actionLabel.setFont(QFont("幼圆",20))
        actionLabel.setText("ACTION")

        self.tableView1=QTableView()
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView1.horizontalHeader().setStretchLastSection(True)
        self.tableView1.verticalHeader().setVisible(False)

        actionVLayout.addWidget(actionLabel)
        actionVLayout.addWidget(self.tableView1)

        hLayout.addLayout(actionVLayout)

        # 表格2
        gotoVLayout=QVBoxLayout()
        gotoLabel=QLabel()
        gotoLabel.setAlignment(Qt.AlignCenter)
        gotoLabel.setFont(QFont("幼圆",20))
        gotoLabel.setText("GOTO")

        self.tableView2=QTableView()
        self.tableView2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView2.horizontalHeader().setStretchLastSection(True)
        self.tableView2.verticalHeader().setVisible(False)

        gotoVLayout.addWidget(gotoLabel)
        gotoVLayout.addWidget(self.tableView2)

        hLayout.addLayout(gotoVLayout)

        self.setLayout(hLayout)


    def calculate(self):
        try:
            res = self.te.toPlainText().split("\n")
            lr0table=LR0Table(res)
            lr0table.getVisibleLR0Table()

            self.model1=QStandardItemModel(len(lr0table.visibleTable_VT)-1,
            len(lr0table.visibleTable_VT[0]))
            self.model1.setHorizontalHeaderLabels(lr0table.visibleTable_VT[0][:])
      
            for row in range(len(lr0table.visibleTable_VT)-1):
                for column in range(1,len(lr0table.visibleTable_VT[0])):
                    item=QStandardItem(lr0table.visibleTable_VT[row+1][column])
                    self.model1.setItem(row,column,item)
            
            for row in range(0,len(lr0table.visibleTable_VT)-1):
                item=QStandardItem(str(row))
                item.setToolTip("state"+str(row)+":\n"+lr0table.lr0.getStateStr(row))
                self.model1.setItem(row,0,item)
                
            
            self.tableView1.setModel(self.model1)

            ### 表格2
            self.model2=QStandardItemModel(len(lr0table.visibleTable_VN)-1,
            len(lr0table.visibleTable_VN[0])-1)
            self.model2.setHorizontalHeaderLabels(lr0table.visibleTable_VN[0][1:])
            

            for row in range(len(lr0table.visibleTable_VN)-1):
                for column in range(len(lr0table.visibleTable_VN[0])-1):
                    item=QStandardItem(lr0table.visibleTable_VN[row+1][column+1])
                    self.model2.setItem(row,column,item)
            self.tableView2.setModel(self.model2)
            
            
        except:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("输入有误，请检查您的输入！")
            errorMessage.exec_()

    def getExample(self):
        self.te.setText("E' → E\nE->(E)\nE->i")

class WidgetUI6(QWidget):
    def __init__(self):
        super().__init__()


class WidgetUI7(QWidget):
    def __init__(self):
        super().__init__()

        # 文法输入框
        self.te = QTextEdit()
        self.te.setPlaceholderText("在此输入文法规则")
        self.te.setFontFamily("幼圆")
        self.te.setFontPointSize(20)

        # 计算按钮
        self.dealButton=QPushButton(self)
        self.dealButton.setText("构造LR(1)分析表")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.dealButton.setToolTip("根据识别文法活前缀的 DFA 构造 LR(1)分析表")
        self.dealButton.resize(self.dealButton.sizeHint())
        # 范例按钮
        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())

        vLayout=QVBoxLayout()
        vLayout.addWidget(self.te)
        vLayout.addWidget(self.dealButton)
        vLayout.addWidget(self.exampleButton)
   
        hLayout=QHBoxLayout()
        hLayout.addLayout(vLayout)

        # 表格1
        actionVLayout=QVBoxLayout()
        actionLabel=QLabel()
        actionLabel.setAlignment(Qt.AlignCenter)
        actionLabel.setFont(QFont("幼圆",20))
        actionLabel.setText("ACTION")

        self.tableView1=QTableView()
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView1.horizontalHeader().setStretchLastSection(True)
        self.tableView1.verticalHeader().setVisible(False)

        actionVLayout.addWidget(actionLabel)
        actionVLayout.addWidget(self.tableView1)

        hLayout.addLayout(actionVLayout)

        # 表格2
        gotoVLayout=QVBoxLayout()
        gotoLabel=QLabel()
        gotoLabel.setAlignment(Qt.AlignCenter)
        gotoLabel.setFont(QFont("幼圆",20))
        gotoLabel.setText("GOTO")

        self.tableView2=QTableView()
        self.tableView2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView2.horizontalHeader().setStretchLastSection(True)
        self.tableView2.verticalHeader().setVisible(False)

        gotoVLayout.addWidget(gotoLabel)
        gotoVLayout.addWidget(self.tableView2)

        hLayout.addLayout(gotoVLayout)

        self.setLayout(hLayout)


    def calculate(self):
        try:
            res = self.te.toPlainText().split("\n")

            lr1=LR1()
            lr1.setGrammar(res)
            lr1Table = LR1Table(lr1)
            printTable=lr1Table.get_visible_table() 

            ## ACTION表
            self.model1=QStandardItemModel(len(lr1Table.lr1.states),
            len(lr1Table.table_VT)+1)
            self.model1.setHorizontalHeaderLabels([' ']+lr1Table.table_VT)
      
            for row in range(len(lr1Table.lr1.states)):
                for col in range(len(lr1Table.table_VT)+1):
                    if col==0:
                        item=QStandardItem(str(row))
                        item.setToolTip("state"+str(row)+":\n"+lr1Table.lr1.getStateStr(row))
                    else:
                        item=QStandardItem(str(printTable[row+1][col]))
                    self.model1.setItem(row,col,item)
            
            self.tableView1.setModel(self.model1)


            ### GOTO表
            self.model2=QStandardItemModel(len(lr1Table.lr1.states),
            len(lr1Table.table_VN))
            self.model2.setHorizontalHeaderLabels(lr1Table.table_VN)

            for row in range(len(lr1Table.lr1.states)):
                for column in range(len(lr1Table.table_VN)):
                    item=QStandardItem(str(printTable[row+1][column+1+len(lr1Table.table_VT)]))
                    self.model2.setItem(row,column,item)
            self.tableView2.setModel(self.model2)
            print(self.model2)
            
        except:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("输入有误，请检查您的输入！")
            errorMessage.exec_()

    def getExample(self):
        self.te.setText("S'->S\nS->BB\nB->aB\nB->b")

class WidgetUI8(QWidget):
    def __init__(self):
        super().__init__()

        # 文法输入框
        self.te = QTextEdit()
        self.te.setPlaceholderText("在此输入文法规则")
        self.te.setFontFamily("幼圆")
        self.te.setFontPointSize(20)

        # 计算按钮
        self.dealButton=QPushButton(self)
        self.dealButton.setText("构造LALR分析表")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.dealButton.setToolTip("根据识别文法活前缀的 DFA 构造 LALR分析表")
        self.dealButton.resize(self.dealButton.sizeHint())
        # 范例按钮
        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())

        vLayout=QVBoxLayout()
        vLayout.addWidget(self.te)
        vLayout.addWidget(self.dealButton)
        vLayout.addWidget(self.exampleButton)
   
        hLayout=QHBoxLayout()
        hLayout.addLayout(vLayout)

        # 表格1
        actionVLayout=QVBoxLayout()
        actionLabel=QLabel()
        actionLabel.setAlignment(Qt.AlignCenter)
        actionLabel.setFont(QFont("幼圆",20))
        actionLabel.setText("ACTION")

        self.tableView1=QTableView()
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView1.horizontalHeader().setStretchLastSection(True)
        self.tableView1.verticalHeader().setVisible(False)

        actionVLayout.addWidget(actionLabel)
        actionVLayout.addWidget(self.tableView1)

        hLayout.addLayout(actionVLayout)

        # 表格2
        gotoVLayout=QVBoxLayout()
        gotoLabel=QLabel()
        gotoLabel.setAlignment(Qt.AlignCenter)
        gotoLabel.setFont(QFont("幼圆",20))
        gotoLabel.setText("GOTO")

        self.tableView2=QTableView()
        self.tableView2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView2.horizontalHeader().setStretchLastSection(True)
        self.tableView2.verticalHeader().setVisible(False)

        gotoVLayout.addWidget(gotoLabel)
        gotoVLayout.addWidget(self.tableView2)

        hLayout.addLayout(gotoVLayout)

        self.setLayout(hLayout)


    def calculate(self):
        try:
            res = self.te.toPlainText().split("\n")

            lr1=LR1()
            lr1.setGrammar(res)
            lalrTable = LALRTable(lr1)

            print(lalrTable.states)

            printTable=lalrTable.get_visible_table()

            ## ACTION表
            self.model1=QStandardItemModel(len(lalrTable.states),
            len(lalrTable.table_VT)+1)
            self.model1.setHorizontalHeaderLabels([' ']+lalrTable.table_VT)
      
            for row in range(len(lalrTable.states)):
                for col in range(len(lalrTable.table_VT)+1):
                    if col==0:
                        item=QStandardItem(str(row))
                        item.setToolTip("state"+str(row)+":\n"+lalrTable.get_state_str(row))
                    else:
                        # 存在与否
                        # if (row,lalrTable.table_VT[col-1]) in lalrTable.state_transfer_array:
                        #     item=QStandardItem(str(printTable[row+1][col]))
                        item=QStandardItem(str(printTable[row+1][col]))
                    self.model1.setItem(row,col,item)
            
            self.tableView1.setModel(self.model1)

            ### GOTO表
            self.model2=QStandardItemModel(len(lalrTable.states),
            len(lalrTable.table_VN))
            self.model2.setHorizontalHeaderLabels(lalrTable.table_VN)

            for row in range(len(lalrTable.states)):
                for column in range(len(lalrTable.table_VN)):
                    item=QStandardItem(str(printTable[row+1][column+1+len(lalrTable.table_VT)]))
                    self.model2.setItem(row,column,item)
            self.tableView2.setModel(self.model2)
            print(self.model2)
            
        except error:
            print(error)
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("输入有误，请检查您的输入！")
            errorMessage.exec_()

    def getExample(self):
        self.te.setText("S'->S\nS->BB\nB->aB\nB->b")


class WidgetUI9(QWidget):
    def __init__(self):
        super().__init__()

        # 文法输入框
        self.te = QTextEdit()
        self.te.setPlaceholderText("在此输入文法规则")
        self.te.setFontFamily("幼圆")
        self.te.setFontPointSize(20)

        # 下拉框
        self.cb=QComboBox()
        self.cb.addItem("LR(0)")


        # 计算按钮
        self.dealButton=QPushButton(self)
        self.dealButton.setText("构造LR分析表")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.dealButton.setToolTip("根据识别文法活前缀的 DFA 构造 LR分析表")
        self.dealButton.resize(self.dealButton.sizeHint())
        # 范例按钮
        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())

        vLayout=QVBoxLayout()
        vLayout.addWidget(self.te)
        vLayout.addWidget(self.dealButton)
        vLayout.addWidget(self.exampleButton)
   
        hLayout=QHBoxLayout()
        hLayout.addLayout(vLayout)

        # 表格1
        actionVLayout=QVBoxLayout()
        actionLabel=QLabel()
        actionLabel.setAlignment(Qt.AlignCenter)
        actionLabel.setFont(QFont("幼圆",20))
        actionLabel.setText("ACTION")

        self.tableView1=QTableView()
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView1.horizontalHeader().setStretchLastSection(True)
        self.tableView1.verticalHeader().setVisible(False)

        actionVLayout.addWidget(actionLabel)
        actionVLayout.addWidget(self.tableView1)

        hLayout.addLayout(actionVLayout)

        # 表格2
        gotoVLayout=QVBoxLayout()
        gotoLabel=QLabel()
        gotoLabel.setAlignment(Qt.AlignCenter)
        gotoLabel.setFont(QFont("幼圆",20))
        gotoLabel.setText("GOTO")

        self.tableView2=QTableView()
        self.tableView2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView2.horizontalHeader().setStretchLastSection(True)
        self.tableView2.verticalHeader().setVisible(False)

        gotoVLayout.addWidget(gotoLabel)
        gotoVLayout.addWidget(self.tableView2)

        hLayout.addLayout(gotoVLayout)

        self.setLayout(hLayout)

    def calculate(self):
        pass

    def getExample(self):
        pass

class ComprehensiveExperiment(QWidget):
    def __init__(self):
        super().__init__()

        # 文法输入框
        self.te = QTextEdit()
        self.te.setPlaceholderText("在此输入文法规则")
        self.te.setFontFamily("幼圆")
        self.te.setFontPointSize(20)

        # 待分析语句
        self.analysisInput=QTextEdit()
        self.analysisInput.setPlaceholderText("在此输入待分析语句")
        self.analysisInput.setFontFamily("幼圆")
        self.analysisInput.setFontPointSize(20)

        # 计算按钮
        self.dealButton=QPushButton(self)
        self.dealButton.setText("构造LR分析表")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.dealButton.setToolTip("根据识别文法活前缀的 DFA 构造 LR分析表")
        self.dealButton.resize(self.dealButton.sizeHint())
        # 范例按钮
        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())

        vLayout=QVBoxLayout()
        vLayout.addWidget(self.te)
        vLayout.addWidget(self.analysisInput)
        vLayout.addWidget(self.dealButton)
        vLayout.addWidget(self.exampleButton)
   
        hLayout=QHBoxLayout()
        hLayout.addLayout(vLayout)

        # 表格1
        analysisOutputVLayout=QVBoxLayout()
        analysisOutputLabel=QLabel()
        analysisOutputLabel.setAlignment(Qt.AlignCenter)
        analysisOutputLabel.setFont(QFont("幼圆",20))
        analysisOutputLabel.setText("规约过程产生式")

        # 规约过程产生式
        self.analysisOutput=QTextEdit()
        self.analysisOutput.setPlaceholderText("暂无结果")
        self.analysisOutput.setFontFamily("幼圆")
        self.analysisOutput.setFontPointSize(20)
        self.analysisOutput.setFocusPolicy(Qt.NoFocus)

        analysisOutputVLayout.addWidget(analysisOutputLabel)
        analysisOutputVLayout.addWidget(self.analysisOutput)

        hLayout.addLayout(analysisOutputVLayout)

        # 输出语法树
        self.imageLabel = QLabel()
        self.imageLabel.setText(" ")
        self.imageLabel.setFixedHeight(500)
        

        hLayout.addWidget(self.imageLabel)

        self.setLayout(hLayout)

    def calculate(self):
        res = self.te.toPlainText().split("\n")
        lr1=LR1()
        lr1.setGrammar(res)
        lr1Table = LR1Table(lr1)
        transferArray=lr1Table.state_transfer_array

        inputList=list(self.analysisInput.toPlainText())
        # 在最后加入'#'表示输入结束
        inputList.append('#')

        # 对文法进行分析
        stateStack=Stack()
        # 初始状态为0
        stateStack.push(0)
        
        # 规约表达式
        reduceSentences=[]

        # 初始输入字符
        curIndex=0
        while True:
            # 获取栈顶元素
            curState=stateStack.peek()
            curInput=inputList[curIndex]
            
            # 是否在action表中
            # 判断是否存在，不存在直接报错
            if (curState,curInput) in lr1Table.action:
                nextAct=lr1Table.action[(curState,curInput)]
                
                if nextAct.action == "shift":
                    stateStack.push(nextAct.state)
                    curIndex+=1
                    print("接受输入"+curInput+",跳转到状态"+str(nextAct.state))
                elif nextAct.action == "reduce":
                    # 使用产生式A->β
                    print("需要使用产生式"+str(nextAct.state)+"进行规约")
                    print(lr1Table.lr1.grammarManager.sentences[nextAct.state])
                    reduceSentence=lr1Table.lr1.grammarManager.sentences[nextAct.state]
                    reduceSentences.append(reduceSentence)
                    # 出栈|β|个状态
                    popLength=len(reduceSentence[1])
                    for i in range(popLength):
                        stateStack.pop()
                    # 获取栈顶元素t
                    curState=stateStack.peek()
                    print("当前状态为"+str(curState))
                    # 获取goto[t,A]
                    nextState=lr1Table.goto[(curState,reduceSentence[0])]
                    # 将其加入栈中
                    stateStack.push(nextState)
                else:
                    # success
                    break

        
            else:
                # 错误处理
                raise Exception("错误!")
            
        # 加入到输出中
        outputStr=""
        for index,item in enumerate(reduceSentences):
            if index!=0:
                outputStr+="\n"
            outputStr+=item[0]+"->"+item[1]
        self.analysisOutput.setText(outputStr)

        # 增加语法树

        

    def getExample(self):
        self.te.setText("E->E+T\nE->T\nT->T*F\nT->F\nF->(E)\nF->i")
        self.analysisInput.setText("i+i*i")

if __name__=='__main__':
    app=QApplication(sys.argv)
    mainForm=MainForm()
    mainForm.show()
    
    sys.exit(app.exec_())