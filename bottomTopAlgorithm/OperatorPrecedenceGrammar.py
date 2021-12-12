# -*- coding: utf-8 -*-
"""
算符优先文法

Created on Sun Dec  5 01:03:06 2021

@author: 1851055 汪明杰
"""

from bottomTopAlgorithm.GrammarManager import GrammarManager
from bottomTopAlgorithm.stack import Stack
from graphviz import Digraph
import uuid

class OperatorPrecedenceGrammar:

    def __init__(self):
        self.grammarManager = GrammarManager()

        #self.grammarManager.getInput()

        # 算符优先级关系
        self.priorityTable = dict()

        # 规约文法数组，存储推导过程所用的产生式
        self.productionTable = []

    def setGrammar(self,sentences):
        self.grammarManager.getStr(sentences,False)

    '''
    为算符文法生成算符之间的优先关系表
    '''

    def getPriorityTable(self):

        if len(self.grammarManager.FIRSTVT) == 0:
            self.grammarManager.getFirstAndLastVT()

        # 遍历每一个产生式
        for sentence in self.grammarManager.sentences:
            # sentence[1]
            for i in range(len(sentence[1]) - 1):
                # sentence[1][i] 和 sentence[1][i+1]的关系

                # Xi 和 Xi+1 都是终结符
                if self.grammarManager.isVT(sentence[1][i]) and \
                        self.grammarManager.isVT(sentence[1][i + 1]):
                    self.priorityTable[(sentence[1][i], sentence[1][i + 1])] = '='

                # i<=n-2 且 Xi 和 Xi+2 都是终结符 但 Xi+1 是非终结符
                if i < len(sentence[1]) - 2 and self.grammarManager.isVT(sentence[1][i]) and \
                        self.grammarManager.isVT(sentence[1][i + 2]) and \
                        self.grammarManager.isVN(sentence[1][i + 1]):
                    self.priorityTable[(sentence[1][i], sentence[1][i + 2])] = '='

                # Xi 为终结符 而 Xi+1为非终结符
                if self.grammarManager.isVT(sentence[1][i]) and \
                        self.grammarManager.isVN(sentence[1][i + 1]):
                    for j in self.grammarManager.FIRSTVT[sentence[1][i + 1]]:
                        self.priorityTable[(sentence[1][i], j)] = '<'

                # Xi 为非终结符 而 Xi+1为终结符
                if self.grammarManager.isVN(sentence[1][i]) and \
                        self.grammarManager.isVT(sentence[1][i + 1]):
                    for j in self.grammarManager.LASTVT[sentence[1][i]]:
                        self.priorityTable[(j, sentence[1][i + 1])] = '>'

        return self.priorityTable

    '''
    3.3为算符文法生成语法分析程序
        输入要分析的字符串
    '''
    def operatorGrammarAnalysis(self, input_str):
        input_str = input_str + '#'
        # 初始化符号栈symnol_stack
        symbol_stack = Stack()
        symbol_stack.push('#')
        symbol_stack.push('#')
        # 初始化指针,对应算法中的指针k
        stack_iterator = 1
        a = ''
        strReader = 0  # 控制字符的读入
        j = 0
        # 需要添加#和任何符号的算符优先关系，#<任何算符
        priority_table = self.priorityTable
        for vt in self.grammarManager.VT:
            priority_table[('#',vt)] = '<'
            priority_table[(vt,'#')] = '>'
            priority_table[('#','#')] = '='
        

        # 建立结点
        imgUrl = "..//outputImage//实验3.3语法树" + str(uuid.uuid1())
        g = Digraph(imgUrl, format="png")
        nodeIndex=0
        nodeList=[]

        while True:
            # 获取栈顶算符，k为栈顶
            a = input_str[strReader]
            print(self.grammarManager.VT)
            if self.grammarManager.isVT(symbol_stack.items[stack_iterator]) :
                j = stack_iterator
            else:
                j = stack_iterator-1
            # 当s[j] > a do,寻找最左素短语
            while priority_table[(symbol_stack.items[j], a)] == '>':
                while True:
                    Q = symbol_stack.items[j]
                    if self.grammarManager.isVT(symbol_stack.items[j-1]) or symbol_stack.items[j-1] == '#':
                        j -= 1
                    else:
                        j -= 2
                    if priority_table[(symbol_stack.items[j], Q)] == '<':
                        break
                # 将S[j+1]...S[k]归约为某个N
                statute_str = self.grammarManager.statute_sentence(symbol_stack.items[j+1:stack_iterator+1])
                self.productionTable.append(statute_str)
                N = ''
                M = ''
                if '->' in statute_str:
                    M = statute_str.split('->')[1]
                    N = statute_str.split('->')[0]
                else:
                    M = statute_str.split('→')[1]
                    N = statute_str.split('→')[0]
                for i in range(stack_iterator-j):
                    symbol_stack.pop()
                stack_iterator = j + 1
                symbol_stack.push(N)

                # 此处勿动，为暂未完成的绘图板块
                # 规约的过程
                # 规约，用A->β来绘图
                # 新增一个A
                g.node(name=str(nodeIndex), label=N,shape="none")
                startIndex=nodeIndex

                # 寻找右侧β的每一个结点
                print(M)
                # for ix in list(M):
                #     findIndex=-1
                #     # 从右往左找
                #     for jx in range(len(nodeList)-1,-1,-1):
                #         if nodeList[jx][1]==ix:
                #             # 找到了
                #             findIndex=jx
                #             break
                #     print("nodeList为"+str(nodeList))
                #     print("想要寻找"+ix)
                #     print(str(nodeList))
                #     if findIndex==-1:
                #         break
                #         raise Exception("绘图错误")
                    
                #     # 获取该结点对应的编号
                #     endIndex=nodeList[findIndex][0]
                #     # 删除该结点
                #     del nodeList[findIndex]

                #     #连接边
                #     g.edge(str(startIndex), str(endIndex))

                # # nodeList最后再加A->β中的A
                # nodeList.append([nodeIndex,N])
                # nodeIndex+=1

                print(symbol_stack.items)
            if priority_table[(symbol_stack.items[j],a)] == '<' or priority_table[(symbol_stack.items[j],a)] == '=':
                stack_iterator = stack_iterator+1
                symbol_stack.push(a)

                if a == "#":
                    break

                # 添加新结点
                g.node(name=str(nodeIndex), label=a,shape="none")
                nodeList.append([nodeIndex,a])
                nodeIndex+=1
                print("nodeList新增结点"+str(nodeList))
            else:
                return "error!"
            
            strReader += 1
        return g



if __name__ == '__main__':
    opg = OperatorPrecedenceGrammar()
    sentences=["E->E+T|T","T->T*F|F","F->P↑F|P","P->(E)|i"]
    opg.grammarManager.getStr(sentences)
    opg.getPriorityTable()
    print(opg.priorityTable)
    opg.operatorGrammarAnalysis("i+i*i")
    print(opg.productionTable)
