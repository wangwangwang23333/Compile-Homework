# -*- coding: utf-8 -*-

"""
文法管理器
@author 1851055 汪明杰
"""

from bottomTopAlgorithm.stack import Stack


class GrammarManager:

    def __init__(self):
        self.VT = []
        self.VN = []
        self.sentences = []
        self.basicFirstSet = dict()
        self.FIRSTVT = dict()
        self.LASTVT = dict()
        print("初始化中")

    # 接受输入
    def getInput(self):
        sentenceNum = int(input())
        self.sentences = []

        for i in range(sentenceNum):
            sentence = input().replace(' ', '').replace('\n', '').replace('\r', '').replace("│", "|")
            # 去除空格、换行符
            if "->" in sentence:
                newSentence = sentence.split("->")
            elif "→" in sentence:
                newSentence = sentence.split("→")
            else:
                print(sentence)
                print("error1")
                raise Exception("不含分隔符")

            if len(newSentence[1]) == 0:
                raise Exception("不含分隔符")

            # 对右侧|进行处理
            sentenceRightSide = newSentence[1].split("|")
            for i in sentenceRightSide:
                self.sentences.append([newSentence[0], i])

        # 计算终结符和非终结符
        self.calculateVTandVN()
        # print(self.sentences)

    # 给定字符串
    def getStr(self, sentences, LRAnalysis = True):
        self.sentences = []
        for i in range(len(sentences)):
            sentence = sentences[i].replace("│", "|").replace(' ', '').replace('\n', '').replace('\r', '')
            if len(sentence)==0:
                continue
            # 去除空格、换行符
            if "->" in sentence:
                newSentence = sentence.split("->")
            elif "→" in sentence:
                newSentence = sentence.split("→")
            else:
                print(sentence)
                print("error1")
                raise Exception("不含分隔符")

            if len(newSentence[1]) == 0:
                raise Exception("不含分隔符")

            # 对右侧|进行处理
            sentenceRightSide = newSentence[1].split("|")
            for i in sentenceRightSide:
                self.sentences.append([newSentence[0], i])

        # 增加拓广文法(LR文法需要)
        if (not "'" in self.sentences[0][0]) and LRAnalysis:
            print("手动增加了拓广文法")
            self.sentences.insert(0, [self.sentences[0][0]+"'",self.sentences[0][0]])

        # 计算终结符和非终结符
        self.calculateVTandVN()

    '''
    计算终结符和非终结符
    '''

    def calculateVTandVN(self):
        if len(self.VT) > 0:
            print("终结符和非终结符已经计算过！")
            return
        for i in range(len(self.sentences)):
            for j in range(2):
                passNext = False
                for k in range(len(self.sentences[i][j])):
                    if passNext:
                        passNext = False
                        continue
                    if self.sentences[i][j][k].isupper():
                        # 大写字母需要考虑下一位是否为'
                        if k + 1 < len(self.sentences[i][j]) and self.sentences[i][j][k + 1] == "'":
                            if not self.sentences[i][j][k:k + 2] in self.VN:
                                self.VN.append(self.sentences[i][j][k:k + 2])
                                passNext = True
                        else:
                            if not self.sentences[i][j][k] in self.VN:
                                self.VN.append(self.sentences[i][j][k])
                    else:
                        # 终结符
                        if self.sentences[i][j][k] == "'":
                            raise Exception("右侧不应该出现'")
                        else:
                            if not self.sentences[i][j][k] in self.VT:
                                self.VT.append(self.sentences[i][j][k])

    def isVT(self, c):
        return c in self.VT

    def isVN(self, c):
        return c in self.VN

    '''
    计算基本First集合
    '''

    def getBasicFirstSet(self):
        if len(self.basicFirstSet) != 0:
            return

        for i in self.VT:
            self.basicFirstSet[i] = set([i])

        for vn in self.VN:
            self.basicFirstSet[vn] = set()
            # 寻找产生式左端等于他的
            for index, item in enumerate(self.sentences):
                if item[0] == vn:
                    # 查看item[1]的最左边第一个字符

                    # ε的情况
                    if item[1] == "ε":
                        self.basicFirstSet[vn].add("ε")

                    # item[1][0]
                    # 查看item[1][0]是终结符                   
                    if item[1][0] in self.VT:
                        self.basicFirstSet[vn].add(item[1][0])
                        continue

        # 终结符的第二轮遍历
        hasGrown = True
        while hasGrown:
            hasGrown = False

            for vn in self.VN:
                for index, item in enumerate(self.sentences):
                    if item[0] == vn:

                        # item[0] -> item[1]

                        # 确定item[1]的形式是否为 X →Y1Y2…Yn
                        for j in item[1]:
                            # j是非终结符
                            if j in self.VT:
                                # 到此为止

                                if not j in self.basicFirstSet[vn]:
                                    hasGrown = True
                                    self.basicFirstSet[vn].add(j)
                                break
                            # j是非终结符
                            if j in self.VN:

                                # 将basicFirstSet[j]中的元素都加入basicFirstSet[vn]中
                                for t in self.basicFirstSet[j]:
                                    if not t in self.basicFirstSet[vn]:
                                        hasGrown = True
                                        self.basicFirstSet[vn].add(t)

                                # 如果j中含有ε，则继续遍历
                                if not "ε" in self.basicFirstSet[j]:
                                    break

                                # 遍历到最后一个时，将ε加入其中
                                if j == self.VN[-1]:
                                    if not "ε" in self.basicFirstSet[vn]:
                                        hasGrown = True
                                        self.basicFirstSet[vn].add("ε")

    '''
    为候选式α计算First集合
    '''

    def getFirstSet(self, initialState):

        # 先计算基本First集合
        self.getBasicFirstSet()

        firstSet = set()
        # α= X1X2… Xn
        for i in initialState:
            # 确定i为终结符还是非终结符

            # 终结符，到此为止
            if i in self.VT:
                firstSet.add(i)
                break

            # 如果i为#，则表示到此为止
            if i == "#":
                firstSet.add('#')
                break

            # 非终结符
            if i in self.VN:
                # 将 self.basicFirstSet[i] 中除了 ε 都加入
                for j in self.basicFirstSet[i]:
                    if j == "ε":
                        continue
                    else:
                        firstSet.add(j)

                # 如果没有ε，就不需要再算下去了
                if not "ε" in self.basicFirstSet[i]:
                    break

            if i == initialState[-1]:
                firstSet.add("ε")

        return firstSet

    '''
    为构造FIRSTVT与LASTVT使用的INSERT方法
    '''

    def insertSymbolPair(self, nonTerminalIndex, terminalIndex, judgmentMatrix, symbolStack):

        if not judgmentMatrix[nonTerminalIndex][terminalIndex]:
            judgmentMatrix[nonTerminalIndex][terminalIndex] = True
            symbolStack.push([nonTerminalIndex, terminalIndex])

    '''
    计算非终结符对应的 FIRSTVT
    因为计算方式相似，所以通过一个函数完成对FIRSTVT与LASTVT的生成
    FIRST choice 表示生成FIRSTVT
    LAST choice 表示生成LASTVT
    '''

    def getFirstVTorLastVT(self, choice):

        # 检测是否有终结符与非终结符
        if len(self.VN) == 0 or len(self.VT) == 0:
            print("输入终结符或非终结符!")
            return

        # 构造二维布尔矩阵F[P,a]和符号栈stack
        judgmentMatrix = [[False for i in range(len(self.VT))] for j in range(len(self.VN))]
        symbolStack = Stack()

        # 接下来遍历sentences然后逐一进行处理入栈
        for sentence in self.sentences:

            # 这里要先进行处理:
            if choice == "LAST":
                tmp = sentence[1]
                sentence[1] = tmp[:: -1]

            # 先获取非终结符
            nonTerminalIndex = self.VN.index(sentence[0])
            # 对非终结符对应的语句进行处理
            if len(sentence[1]) != 0:
                # 获得首元素
                firstSymbol = sentence[1][0]
                # 如果首元素是终结符
                if firstSymbol in self.VT:
                    firstSymbolIndex = self.VT.index(firstSymbol)
                    # 修改矩阵并且插入到符号栈 对应 P->a...情况
                    self.insertSymbolPair(nonTerminalIndex, firstSymbolIndex, judgmentMatrix, symbolStack)
                elif firstSymbol in self.VN:
                    if len(sentence[1]) >= 2:
                        secondSymbol = sentence[1][1]
                        if secondSymbol in self.VT:
                            secondSymbolIndex = self.VT.index(secondSymbol)
                            # 修改矩阵并插入到符号栈 对应P->Qa...的情况
                            self.insertSymbolPair(nonTerminalIndex, secondSymbolIndex, judgmentMatrix, symbolStack)
                else:
                    raise Exception("生成FIRSTVT过程出现错误!")

        # 循环处理Stack的过程
        while not symbolStack.is_empty():
            # 获得栈顶元素
            symbolPair = symbolStack.pop()
            symbolPairNT = self.VN[symbolPair[0]]
            for s in self.sentences:
                if choice == "LAST":
                    tmp = s[1]
                    s[1] = tmp[:: -1]
                if len(s[1]) != 0 and s[1][0] == symbolPairNT:
                    self.insertSymbolPair(self.VN.index(s[0]), symbolPair[1], judgmentMatrix, symbolStack)
                    # 结束循环得到结果
        result = {}
        for index, teminalList in enumerate(judgmentMatrix):
            VTs = []
            for i, flag in enumerate(teminalList):
                if flag:
                    VTs.append(self.VT[i])
            result[self.VN[index]] = VTs

        return result

    def getFirstAndLastVT(self):

        self.FIRSTVT = self.getFirstVTorLastVT("FIRST")

        self.LASTVT = self.getFirstVTorLastVT("LAST")

    def get_number_of_sentence(self, sentence):
        """
        3.5 之后的算法都拓展一列规约产生式的编号，通过这个函数，可以获得算法中所用的四元产生式（state）的产生式编号
        :param sentence: 的格式是 [左侧, 右侧, 当前位置, 接受字符]
        :return: sentence 的产生式编号
        """
        s = [sentence[0], sentence[1]]
        if s not in self.sentences:
            raise Exception("不存在的产生式")
        # 从0开始，本身就是数组下标
        return self.sentences.index(s)

    '''
    给定一个句子，将其进行规约
    返回成功规约的文法串
    '''
    def statute_sentence(self,sentence_pattern):
        result_set = ""
        print(self.sentences)
        for grammar_sentence in self.sentences:
            compare_sentence = grammar_sentence[1]
            if len(compare_sentence) == len(sentence_pattern):
                math_tag = 1
                for i in range(0,len(compare_sentence)):
                    if (sentence_pattern[i] in self.VT and sentence_pattern[i] == compare_sentence[i]) or (sentence_pattern[i] not in self.VT and compare_sentence[i] in self.VN ):  # 终结符对终结符，非终结符对非终结符
                        continue
                    else:
                        math_tag = 0
                if math_tag == 1:
                    result_set = grammar_sentence[0]+"→"+grammar_sentence[1]
        return result_set

if __name__ == '__main__':
    g = GrammarManager()
    g.getInput()
    # print(g.get_number_of_sentence(['E', 'i']))
