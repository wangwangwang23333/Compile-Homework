# -*- coding: utf-8 -*-
"""
算符优先文法

Created on Sun Dec  5 01:03:06 2021

@author: 1851055 汪明杰
"""

from bottomTopAlgorithm.GrammarManager import GrammarManager
from bottomTopAlgorithm.stack import Stack


class OperatorPrecedenceGrammar:

    def __init__(self):
        self.grammarManager = GrammarManager()

        #self.grammarManager.getInput()

        # 算符优先级关系
        self.priorityTable = dict()

        # 规约文法数组，存储推导过程所用的产生式
        self.productionTable = []

    def setGrammar(self,sentences):
        self.grammarManager.getStr(sentences)

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
        # 初始化符号栈
        S = Stack()
        S.push('#')
        S.push('#')
        # 初始化指针
        k = 1
        a = ''
        strReader = 0  # 控制字符的读入
        j = 0
        # 需要添加#和任何符号的算符优先关系，#<任何算符
        priority_table = self.priorityTable
        for str in self.grammarManager.VT:
            priority_table[('#',str)] = '<'
            priority_table[(str,'#')] = '>'
            priority_table[('#','#')] = '='

        while True:
            # 获取栈顶算符，k为栈顶
            a = input_str[strReader]
            print(self.grammarManager.VT)
            if self.grammarManager.isVT(S.items[k]) :
                j = k
            else:
                j = k-1
            # 当s[j] > a do,寻找最左素短语
            while priority_table[(S.items[j], a)] == '>':
                while True:
                    Q = S.items[j]
                    if self.grammarManager.isVT(S.items[j-1]) or S.items[j-1] == '#':
                        j -= 1
                    else:
                        j -= 2
                    if priority_table[(S.items[j], Q)] == '<':
                        break
                # 将S[j+1]...S[k]归约为某个N
                statute_str = self.grammarManager.statute_sentence(S.items[j+1:k+1])
                self.productionTable.append(statute_str)
                N = ''
                if '->' in statute_str:
                    N = statute_str.split('->')[0]
                else:
                    N = statute_str.split('→')[0]
                for i in range(k-j):
                    S.pop()
                k = j + 1
                S.push(N)
                print(S.items)
            if priority_table[(S.items[j],a)] == '<' or priority_table[(S.items[j],a)] == '=':
                k = k+1
                S.push(a)
            else:
                return "error!"
            if a == "#":
                break
            strReader += 1
        return "success!"











if __name__ == '__main__':
    opg = OperatorPrecedenceGrammar()
    sentences=["E->E+T|T","T->T*F|F","F->P↑F|P","P->(E)|i"]
    opg.grammarManager.getStr(sentences)
    opg.getPriorityTable()
    print(opg.priorityTable)
    opg.operatorGrammarAnalysis("i+i*i")
    print(opg.productionTable)
