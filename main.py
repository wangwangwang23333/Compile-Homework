# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:09:34 2021

@author: 1851055 汪明杰
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
import uuid
from graphviz import Digraph

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
        self.te.setPlaceholderText("在此输入文法规则")
        label1=QLabel("输入文法规则",self)
        label1.move(50,170)


        self.outputArea = QTextEdit(self)
        self.outputArea.move(600,200)
        self.outputArea.setReadOnly(True)
        label2=QLabel("输出",self)
        label2.move(600,170)
        self.outputArea.setPlaceholderText("此处为输出")

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
            g.getStr(res,False)

            g.getFirstAndLastVT()
            
            outputStr="FirstVT:\n"
            for i in g.FIRSTVT:
                outputStr+=str(i)+":"+str(g.FIRSTVT[i])+"\n"

            outputStr+="\nLastVT:\n"
            for i in g.LASTVT:
                outputStr+=str(i)+":"+str(g.LASTVT[i])+"\n"   
            self.outputArea.setText(outputStr)
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

        self.g=None

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
        self.dealButton.setText("语法分析")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.dealButton.setToolTip("为算符文法生成语法分析程序，并对语法进行分析")
        self.dealButton.resize(self.dealButton.sizeHint())
        # 范例按钮
        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())

        self.saveButton=QPushButton(self)
        self.saveButton.setText("保存图片")
        self.saveButton.clicked.connect(self.saveImage)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.saveButton.setToolTip("您可以保存生成的语法树")
        self.saveButton.resize(self.saveButton.sizeHint())

        vLayout=QVBoxLayout()
        vLayout.addWidget(self.te)
        vLayout.addWidget(self.analysisInput)
        vLayout.addWidget(self.dealButton)
        vLayout.addWidget(self.exampleButton)
        vLayout.addWidget(self.saveButton)
   
        hLayout=QHBoxLayout()
        hLayout.addLayout(vLayout)

        # 表格1
        analysisOutputVLayout=QVBoxLayout()
        analysisOutputLabel=QLabel()
        analysisOutputLabel.setAlignment(Qt.AlignCenter)
        analysisOutputLabel.setFont(QFont("幼圆",20))
        analysisOutputLabel.setText("推导过程产生式")

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
        self.imageLabel.setFixedHeight(450)
        

        hLayout.addWidget(self.imageLabel)

        self.setLayout(hLayout)

    def calculate(self):
        res = self.te.toPlainText().split("\n")
        opg=OperatorPrecedenceGrammar()
        opg.setGrammar(res)
        opg.getPriorityTable()

        
        inputText=self.analysisInput.toPlainText()
        baseUrl,self.g=opg.operatorGrammarAnalysis(inputText)

        baseUrl="outputImage//"+baseUrl
        self.g.render(baseUrl)
        self.imgUrl=baseUrl+".png"
        
        # 加载图片
        DFAImage = QPixmap(self.imgUrl).scaledToHeight(450)
        self.imageLabel.setPixmap(DFAImage)

        outputStr=""
        for index,item in enumerate(opg.productionTable):
            if index!=0:
                outputStr+="\n"
            outputStr+=item
        self.analysisOutput.setText(outputStr)
        
        # self.g.view()

    def saveImage(self):
        if self.g==None:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("请先生成语法树！")
            errorMessage.exec_()
            return
        self.g.view()
                
        

    def getExample(self):
        self.te.setText("E->E+T|T\nT->T*F|F\nF->P↑F|P\nP->(E)|i")
        self.analysisInput.setText("i+i*i")

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
            
        except:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("输入有误，请检查您的输入！")
            errorMessage.exec_()

    def getExample(self):
        self.te.setText("S'->S\nS->BB\nB->aB\nB->b")


class WidgetUI9(QWidget):
    def __init__(self):
        super().__init__()

        self.g=None

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
        calculateHLayout=QHBoxLayout()
        self.analysisButton=QPushButton(self)
        self.analysisButton.setText("解析文法")
        self.analysisButton.clicked.connect(self.analysisGrammar)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.analysisButton.setToolTip("解析文法，产生状态表初始状态")
        self.analysisButton.resize(self.analysisButton.sizeHint())
        calculateHLayout.addWidget(self.analysisButton)

        self.dealButton=QPushButton()
        self.dealButton.setText("语法分析")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.dealButton.setToolTip("解析文法，产生状态表初始状态")
        calculateHLayout.addWidget(self.dealButton)
        self.dealButton.setEnabled(False)


        # 范例按钮
        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())

        self.saveButton=QPushButton(self)
        self.saveButton.setText("保存图片")
        self.saveButton.clicked.connect(self.saveImage)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.saveButton.setToolTip("您可以保存生成的语法树")
        self.saveButton.resize(self.saveButton.sizeHint())

        # 按钮
        buttonHLayout=QHBoxLayout()
        self.addRowButton=QPushButton()
        self.addRowButton.setText("添加一行")
        self.addRowButton.clicked.connect(self.addRow)
        self.addRowButton.setEnabled(False)
        buttonHLayout.addWidget(self.addRowButton)
        self.removeRowButton=QPushButton()
        self.removeRowButton.setText("删除一行")
        self.removeRowButton.clicked.connect(self.removeRow)
        self.removeRowButton.setEnabled(False)
        buttonHLayout.addWidget(self.removeRowButton)

        vLayout=QVBoxLayout()
        vLayout.addWidget(self.te)
        vLayout.addWidget(self.analysisInput)
        vLayout.addLayout(calculateHLayout)
        vLayout.addWidget(self.exampleButton)
        vLayout.addWidget(self.saveButton)
        vLayout.addLayout(buttonHLayout)
   
        hLayout=QHBoxLayout()
        hLayout.addLayout(vLayout)

        # 建立一个竖直方向的layout
        tableVLayout=QVBoxLayout()

        # 建立一个表格的水平layout
        tableHLayout=QHBoxLayout()

        # 表格1
        actionVLayout=QVBoxLayout()
        actionLabel=QLabel()
        actionLabel.setAlignment(Qt.AlignCenter)
        actionLabel.setFont(QFont("幼圆",20))
        actionLabel.setText("ACTION")

        self.tableView1=QTableView()
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView1.horizontalHeader().setStretchLastSection(True)
        # self.tableView1.verticalHeader().setVisible(False)

        actionVLayout.addWidget(actionLabel)
        actionVLayout.addWidget(self.tableView1)

        tableHLayout.addLayout(actionVLayout)

        # 表格2
        gotoVLayout=QVBoxLayout()
        gotoLabel=QLabel()
        gotoLabel.setAlignment(Qt.AlignCenter)
        gotoLabel.setFont(QFont("幼圆",20))
        gotoLabel.setText("GOTO")

        self.tableView2=QTableView()
        self.tableView2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView2.horizontalHeader().setStretchLastSection(True)
        # self.tableView2.verticalHeader().setVisible(False)

        gotoVLayout.addWidget(gotoLabel)
        gotoVLayout.addWidget(self.tableView2)

        tableHLayout.addLayout(gotoVLayout)

        #表格竖直视图
        tableVLayout.addLayout(tableHLayout)

        # 表格下方加入文法分析结果
        self.analysisOutput=QTextEdit()
        self.analysisOutput.setPlaceholderText("暂无结果")
        self.analysisOutput.setFontFamily("幼圆")
        self.analysisOutput.setFontPointSize(20)
        self.analysisOutput.setFocusPolicy(Qt.NoFocus)

        tableVLayout.addWidget(self.analysisOutput)


        hLayout.addLayout(tableVLayout)

        # 输出语法树
        self.imageLabel = QLabel()
        self.imageLabel.setText(" ")
        self.imageLabel.setFixedHeight(500)

        hLayout.addWidget(self.imageLabel)


        self.setLayout(hLayout)

    def calculate(self):
        try:
            # 计算
            # 绘制语法树
            imgUrl = 'outputImage//实验3.9语法树' + str(uuid.uuid1())
            g = Digraph(imgUrl, format="png")
            nodeIndex=0
            nodeList=[]

            # 输入字符
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
                
                print((curState,curInput))
                # 获取curInput在VT中的位置
                curInputCol=self.VT.index(curInput)

                print(self.model1.item(curState,curInputCol).text())

                # 获取其对应的act
                nextAct=self.model1.item(curState,curInputCol).text()

                if nextAct=="":
                    raise Exception("错误的输入")    
                
                if nextAct[0] == "s":
                    stateStack.push(int(nextAct[1:]))
                    curIndex+=1
                    print("接受输入"+curInput+",跳转到状态"+nextAct[1:])

                    # 移进，则往语法树中增加新的结点
                    g.node(name=str(nodeIndex), label=curInput,shape="none")
                    nodeList.append([nodeIndex,curInput])
                    nodeIndex+=1
                    print("nodeList新增结点"+str(nodeList))

                elif nextAct[0] == "r":
                    # 使用产生式A->β
                    print("需要使用产生式"+nextAct[1:]+"进行规约")
                    print(self.grammarManager.sentences[int(nextAct[1:])])
                    reduceSentence=self.grammarManager.sentences[int(nextAct[1:])]
                    reduceSentences.append(reduceSentence)
                    # 出栈|β|个状态
                    popLength=len(reduceSentence[1])
                    for i in range(popLength):
                        stateStack.pop()
                    # 获取栈顶元素t
                    curState=stateStack.peek()
                    print("当前状态为"+str(curState)+",正在接收输入"+reduceSentence[0])
                    
                    print(self.VN.index(reduceSentence[0]))
                    
                    # 获取goto[t,A]
                    nextState=self.model2.item(curState,self.VN.index(reduceSentence[0])).text()
                    nextState=int(nextState)

                    # 将其加入栈中
                    stateStack.push(nextState)

                    # 规约，用A->β来绘图
                    # 新增一个A
                    g.node(name=str(nodeIndex), label=reduceSentence[0],shape="none")
                    startIndex=nodeIndex

                    # 寻找右侧β的每一个结点
                    for i in list(reduceSentence[1]):
                        findIndex=-1
                        # 从右往左找
                        for j in range(len(nodeList)-1,-1,-1):
                            if nodeList[j][1]==i:
                                # 找到了
                                findIndex=j
                                break
                        print("nodeList为"+str(nodeList))
                        if findIndex==-1:
                            raise Exception("绘图错误")
                        
                        # 获取该结点对应的编号
                        endIndex=nodeList[findIndex][0]
                        # 删除该结点
                        del nodeList[findIndex]

                        #连接边
                        g.edge(str(startIndex), str(endIndex))

                    # nodeList最后再加A->β中的A
                    nodeList.append([nodeIndex,reduceSentence[0]])
                    nodeIndex+=1

                else:
                    # success
                    break
            
            print(reduceSentences)
            # 加入到输出中
            outputStr=""
            for index,item in enumerate(reduceSentences):
                if index!=0:
                    outputStr+="\n"
                outputStr+=item[0]+"->"+item[1]
            self.analysisOutput.setText(outputStr)

            g.render(imgUrl)

            DFAImage = QPixmap(imgUrl+".png").scaledToHeight(500)
            self.imageLabel.setPixmap(DFAImage)
            self.g=g
        except:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("输入有误，请检查您的输入！")
            errorMessage.exec_()

    def getExample(self):
        self.te.setText("S->E\nE->E+T\nE->T\nT->T*F\nT->F\nF->(E)\nF->i")
        self.analysisInput.setText("i+i*i")

        self.analysisGrammar()

        # 填充Action和Goto表

        # 0~11行 + * ( ) i #
        self.model1.setItem(0,4,QStandardItem("s5")) # i
        self.model1.setItem(0,2,QStandardItem("s4")) # (
        self.model1.setItem(1,0,QStandardItem("s6")) # +
        self.model1.setItem(1,5,QStandardItem("acc")) # #
        self.model1.setItem(2,0,QStandardItem("r2")) # +
        self.model1.setItem(2,1,QStandardItem("s7")) # *
        self.model1.setItem(2,3,QStandardItem("r2")) # )
        self.model1.setItem(2,5,QStandardItem("r2")) # #
        self.model1.setItem(3,0,QStandardItem("r4")) # +
        self.model1.setItem(3,1,QStandardItem("r4")) # *
        self.model1.setItem(3,3,QStandardItem("r4")) # )
        self.model1.setItem(3,5,QStandardItem("r4")) # #
        self.model1.setItem(4,4,QStandardItem("s5")) # i
        self.model1.setItem(4,2,QStandardItem("s4")) # (
        self.model1.setItem(5,0,QStandardItem("r6")) # +
        self.model1.setItem(5,1,QStandardItem("r6")) # *
        self.model1.setItem(5,3,QStandardItem("r6")) # )
        self.model1.setItem(5,5,QStandardItem("r6")) # #
        self.model1.setItem(6,4,QStandardItem("s5")) # i
        self.model1.setItem(6,2,QStandardItem("s4")) # (
        self.model1.setItem(7,4,QStandardItem("s5")) # i
        self.model1.setItem(7,2,QStandardItem("s4")) # (
        self.model1.setItem(8,0,QStandardItem("s6")) # +
        self.model1.setItem(8,3,QStandardItem("s11")) # )
        self.model1.setItem(9,0,QStandardItem("r1")) # +
        self.model1.setItem(9,1,QStandardItem("s7")) # *
        self.model1.setItem(9,3,QStandardItem("r1")) # )
        self.model1.setItem(9,5,QStandardItem("r1")) # #
        self.model1.setItem(10,0,QStandardItem("r3")) # +
        self.model1.setItem(10,1,QStandardItem("r3")) # *
        self.model1.setItem(10,3,QStandardItem("r3")) # )
        self.model1.setItem(10,5,QStandardItem("r3")) # #
        self.model1.setItem(11,0,QStandardItem("r5")) # +
        self.model1.setItem(11,1,QStandardItem("r5")) # *
        self.model1.setItem(11,3,QStandardItem("r5")) # )
        self.model1.setItem(11,5,QStandardItem("r5")) # #
        

        self.model2.setItem(0,1,QStandardItem("1"))
        self.model2.setItem(0,2,QStandardItem("2"))
        self.model2.setItem(0,3,QStandardItem("3"))
        self.model2.setItem(4,1,QStandardItem("8"))
        self.model2.setItem(4,2,QStandardItem("2"))
        self.model2.setItem(4,3,QStandardItem("3"))
        self.model2.setItem(6,2,QStandardItem("9"))
        self.model2.setItem(6,3,QStandardItem("3"))
        self.model2.setItem(7,3,QStandardItem("10"))

        self.model1.setVerticalHeaderLabels([str(i) for i in range(12)])
        self.model2.setVerticalHeaderLabels([str(i) for i in range(12)])

        self.curTableRow=12
        


    def addRow(self):
        for row in range(self.curTableRow,self.curTableRow+1):
            for col in range(len(self.grammarManager.VT)+1):
                item=QStandardItem("")
                self.model1.setItem(row,col,item)
            for col in range(len(self.grammarManager.VN)):
                item=QStandardItem("")
                self.model2.setItem(row,col,item)
        self.curTableRow+=1
        self.model1.setVerticalHeaderLabels([str(i) for i in range(self.curTableRow)])
        self.model2.setVerticalHeaderLabels([str(i) for i in range(self.curTableRow)])

    def removeRow(self):
        if self.curTableRow == 0:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("当前只有一行，无法继续删除！")
            errorMessage.exec_()
            return

        self.curTableRow-=1
        self.model1.removeRow(self.curTableRow)
        self.model2.removeRow(self.curTableRow)
    
    def analysisGrammar(self):
        try:
            res = self.te.toPlainText().split("\n")
            self.grammarManager=GrammarManager()
            self.grammarManager.getStr(res,False)
            print(self.grammarManager.VT)
            print(self.grammarManager.VN)

            ## ACTION表
            self.model1=QStandardItemModel(1, len(self.grammarManager.VT)+1)
            self.model1.setVerticalHeaderLabels(['0'])
            self.model1.setHorizontalHeaderLabels(self.grammarManager.VT+['#'])

            # 记录，便于后续处理
            self.VT=self.grammarManager.VT+['#']
            self.VN=self.grammarManager.VN
        
            for row in range(1):
                for col in range(len(self.grammarManager.VT)+1):
                    item=QStandardItem("")
                    self.model1.setItem(row,col,item)
            
            self.tableView1.setModel(self.model1)

            ### GOTO表
            self.model2=QStandardItemModel(1, len(self.grammarManager.VN))
            self.model2.setVerticalHeaderLabels(['0'])
            self.model2.setHorizontalHeaderLabels(self.grammarManager.VN)
        
            for row in range(1):
                for col in range(len(self.grammarManager.VN)):
                    item=QStandardItem("")
                    self.model2.setItem(row,col,item)
            
            self.tableView2.setModel(self.model2)

            self.curTableRow=1

            self.addRowButton.setEnabled(True)
            self.removeRowButton.setEnabled(True)
            self.dealButton.setEnabled(True)
        except:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("请输入合理的文法产生式！")
            errorMessage.exec_()

    def saveImage(self):
        if self.g==None:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("请先生成语法树！")
            errorMessage.exec_()
            return
        self.g.view()

class ComprehensiveExperiment(QWidget):
    def __init__(self):
        super().__init__()

        self.g=None

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
        self.dealButton.setText("语法分析")
        self.dealButton.clicked.connect(self.calculate)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.dealButton.setToolTip("根据识别文法活前缀的 DFA 构造 LR(1)分析表，并对语法进行分析")
        self.dealButton.resize(self.dealButton.sizeHint())
        # 范例按钮
        self.exampleButton=QPushButton(self)
        self.exampleButton.setText("范例")
        self.exampleButton.clicked.connect(self.getExample)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.exampleButton.setToolTip("为了便于测试，我们准备了一个范例")
        self.exampleButton.resize(self.exampleButton.sizeHint())

        self.saveButton=QPushButton(self)
        self.saveButton.setText("保存图片")
        self.saveButton.clicked.connect(self.saveImage)
        QToolTip.setFont(QFont('SansSerif', 15))
        self.saveButton.setToolTip("您可以保存生成的语法树")
        self.saveButton.resize(self.saveButton.sizeHint())

        vLayout=QVBoxLayout()
        vLayout.addWidget(self.te)
        vLayout.addWidget(self.analysisInput)
        vLayout.addWidget(self.dealButton)
        vLayout.addWidget(self.exampleButton)
        vLayout.addWidget(self.saveButton)
   
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
        try:
            res = self.te.toPlainText().split("\n")
            lr1=LR1()
            lr1.setGrammar(res)
            lr1Table = LR1Table(lr1)
            transferArray=lr1Table.state_transfer_array

            # 绘制语法树
            imgUrl = 'outputImage//综合实验语法树' + str(uuid.uuid1())
            g = Digraph(imgUrl, format="png")
            nodeIndex=0
            nodeList=[]

            # 输入字符
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

                        # 移进，则往语法树中增加新的结点
                        g.node(name=str(nodeIndex), label=curInput,shape="none")
                        nodeList.append([nodeIndex,curInput])
                        nodeIndex+=1
                        print("nodeList新增结点"+str(nodeList))

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

                        # 规约，用A->β来绘图
                        # 新增一个A
                        g.node(name=str(nodeIndex), label=reduceSentence[0],shape="none")
                        startIndex=nodeIndex

                        # 寻找右侧β的每一个结点
                        for i in list(reduceSentence[1]):
                            findIndex=-1
                            # 从右往左找
                            for j in range(len(nodeList)-1,-1,-1):
                                if nodeList[j][1]==i:
                                    # 找到了
                                    findIndex=j
                                    break
                            print("nodeList为"+str(nodeList))
                            if findIndex==-1:
                                raise Exception("绘图错误")
                            
                            # 获取该结点对应的编号
                            endIndex=nodeList[findIndex][0]
                            # 删除该结点
                            del nodeList[findIndex]

                            #连接边
                            g.edge(str(startIndex), str(endIndex))

                        # nodeList最后再加A->β中的A
                        nodeList.append([nodeIndex,reduceSentence[0]])
                        nodeIndex+=1

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

            print(imgUrl)
            g.render(imgUrl)

            DFAImage = QPixmap(imgUrl+".png").scaledToHeight(500)
            self.imageLabel.setPixmap(DFAImage)
            self.g=g
        except:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("输入有误，请检查您的输入！")
            errorMessage.exec_()
        

    def saveImage(self):
        if self.g==None:
            errorMessage=QMessageBox()
            errorMessage.setWindowTitle("错误")
            errorMessage.setText("请先生成语法树！")
            errorMessage.exec_()
            return
        self.g.view()
                
        

    def getExample(self):
        self.te.setText("E->E+T\nE->T\nT->T*F\nT->F\nF->(E)\nF->i")
        self.analysisInput.setText("i+i*i")

if __name__=='__main__':
    app=QApplication(sys.argv)
    mainForm=MainForm()
    mainForm.show()
    
    sys.exit(app.exec_())