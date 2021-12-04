# -*- coding: utf-8 -*-

"""
文法管理器
@author 1851055 汪明杰
"""
class GrammarManager:
    
    def __init__(self):
        self.VT=[]
        self.VN=[]
        self.basicFirstSet=dict()
        print("初始化中")
    
    # 接受输入
    def getInput(self):
        sentenceNum=int(input())
        self.sentences=[]
        
        for i in range(sentenceNum):
            sentence=input().replace(' ', '').replace('\n', '').replace('\r', '')
            # 去除空格、换行符
            if "->" in sentence:
                newSentence=sentence.split("->")
            elif "→" in sentence:
                newSentence=sentence.split("->")
            else:
                print(sentence)
                print("error1")
            
            #对右侧|进行处理
            sentenceRightSide=newSentence[1].split("|")
            for i in sentenceRightSide:
                self.sentences.append([newSentence[0],i])
                
        # 计算终结符和非终结符
        self.calculateVTandVN()
    
    '''
    计算终结符和非终结符
    '''
    def calculateVTandVN(self):
        if len(self.VT)>0:
            print("终结符和非终结符已经计算过！")
            return
        for i in range(len(self.sentences)):
            for j in range(2):
                passNext=False
                for k in range(len(self.sentences[i][j])):
                    if passNext:
                        passNext=False
                        continue
                    if self.sentences[i][j][k].isupper():
                        # 大写字母需要考虑下一位是否为'
                        if k+1<len(self.sentences[i][j]) and self.sentences[i][j][k+1]=="'":
                            if not self.sentences[i][j][k:k+2] in self.VN:
                                self.VN.append(self.sentences[i][j][k:k+2])
                                passNext=True
                        else:
                            if not self.sentences[i][j][k] in self.VN:
                                self.VN.append(self.sentences[i][j][k])
                    else:
                        # 终结符
                        if self.sentences[i][j][k]=="'":
                            print("error2")
                        else:
                            if not self.sentences[i][j][k] in self.VT:
                                self.VT.append(self.sentences[i][j][k])
    
    
    '''
    计算基本First集合
    '''
    def getBasicFirstSet(self):
        if len(self.basicFirstSet)!=0:
            return
        
        for i in self.VT:
            self.basicFirstSet[i]=set([i])
        
        for vn in self.VN:
            self.basicFirstSet[vn]=set()
            # 寻找产生式左端等于他的
            for index,item in enumerate(self.sentences):
                if item[0]==vn:
                    # 查看item[1]的最左边第一个字符
                    
                    # ε的情况
                    if item[1]=="ε":
                        self.basicFirstSet[vn].add("ε")

                    
                    # item[1][0]
                    # 查看item[1][0]是终结符                   
                    if item[1][0] in self.VT:
                        self.basicFirstSet[vn].add(item[1][0])
                        continue
                    
        # 终结符的第二轮遍历
        hasGrown=True
        while hasGrown:
            hasGrown=False
            
            for vn in self.VN:
                for index,item in enumerate(self.sentences):
                    if item[0]==vn:
                        
                        # item[0] -> item[1]
                        
                        # 确定item[1]的形式是否为 X →Y1Y2…Yn
                        for j in item[1]:
                            # j是非终结符
                            if j in self.VT:
                                # 到此为止
                                
                                if not j in self.basicFirstSet[vn]:
                                    hasGrown=True
                                    self.basicFirstSet[vn].add(j)
                                break
                            # j是非终结符
                            if j in self.VN:
                                
                                # 将basicFirstSet[j]中的元素都加入basicFirstSet[vn]中
                                for t in self.basicFirstSet[j]:
                                    if not t in self.basicFirstSet[vn]:
                                        hasGrown=True
                                        self.basicFirstSet[vn].add(t)
                                    
                                
                                # 如果j中含有ε，则继续遍历
                                if not "ε" in self.basicFirstSet[j]:
                                    break
                                
                                # 遍历到最后一个时，将ε加入其中
                                if j==self.VN[-1]:
                                    if not "ε" in self.basicFirstSet[vn]:
                                        hasGrown=True
                                        self.basicFirstSet[vn].add("ε")
      
    
    
    '''
    为候选式α计算First集合
    '''
    def getFirstSet(self,initialState):
        
        # 先计算基本First集合
        self.getBasicFirstSet()
        
        firstSet=set()
        # α= X1X2… Xn
        for i in initialState:
            # 确定i为终结符还是非终结符
            
            # 终结符，到此为止
            if i in self.VT:
                firstSet.add(i)
                break
            
            # 非终结符
            if i in self.VN:
                # 将 self.basicFirstSet[i] 中除了 ε 都加入
                for j in self.basicFirstSet[i]:
                    if j=="ε":
                        continue
                    else:
                        firstSet.add(j)
            
            if i==initialState[-1]:
                firstSet.add("ε")
        
        return firstSet
 
    # TODO: 王立友3.1
    def getFirstVT(self):
        pass
    
    
    # TODO：王立友3.1
    def getLastVT(self):
        pass

if __name__=='__main__':
    g=GrammarManager()
    g.getInput()
    