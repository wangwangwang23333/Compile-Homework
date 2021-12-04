# -*- coding: utf-8 -*-
"""
算符优先文法

Created on Sun Dec  5 01:03:06 2021

@author: 1851055 汪明杰
"""

from GrammarManager import GrammarManager


class OperatorPrecedenceGrammar:

    def __init__(self):
        self.grammarManager = GrammarManager()

        self.grammarManager.getInput()

        # 算符优先级关系
        self.priorityTable = dict()

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


if __name__ == '__main__':
    opg = OperatorPrecedenceGrammar()
    opg.getPriorityTable()
    print(opg.priorityTable)
