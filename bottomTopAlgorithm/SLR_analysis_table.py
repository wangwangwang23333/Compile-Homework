"""
SLR 分析表构造类
@author: lq
"""

from bottomTopAlgorithm.LRk_state_transfer_generation import LR0
from bottomTopAlgorithm.LR0_analysis_table import LR0Table


class SLRTable:
    """
    输入文法初始化SLRTable类
    """

    def __init__(self, sentences):
        self.lr0 = LR0()
        self.lr0.grammarManager.getStr(sentences,False)
        self.lr0.calculateDFA()
        self.VN = self.lr0.grammarManager.VN
        self.VN = self.VN[1:]
        self.VT = self.lr0.grammarManager.VT
        self.VT.append('#')
        self.action = [[["", -1] for i in range(len(self.VT))] for j in
                       range(len(self.lr0.states))]
        self.goto = [[-1 for i in range(len(self.VN))] for j in range(len(self.lr0.states))]
        #  初始状态action表每个表位置元素均为['',-1],每个goto表状态均为-1
        # 计算follow集合
        self.lr0.grammarManager.calculate_follow()
        self.FollowSet = self.lr0.grammarManager.FOLLOWSET

    '''
    算法3.6：构造slr分析表
    输入：文法（初始化提供），状态转移矩阵（初始化计算）
    输出：SLR分析表，可直接转化为可视化action，goto表
    '''

    def get_SLR_analysis_table(self):
        # 遍历每一个状态的项目集
        dfa_state_array = self.lr0.states
        for Ik_set in range(len(dfa_state_array)):

            for project_sentence in dfa_state_array[Ik_set]:  # 对IK项目集的每一个项目
                # 条件1：项目A->α·aβ属于Ik
                if project_sentence[2] < len(project_sentence[1]) and project_sentence[1][project_sentence[2]] in self.VT:
                    alpha_VT = project_sentence[1][project_sentence[2]]
                    go_result = self.lr0.translationArray[(Ik_set, alpha_VT)]
                    self.action[Ik_set][self.VT.index(alpha_VT)][0] = 's'
                    self.action[Ik_set][self.VT.index(alpha_VT)][1] = go_result
                    continue
                # 条件2：A->α·属于Ik
                if project_sentence[2] == len(project_sentence[1]) and project_sentence[0] in self.VN:
                    for VT_symbol in self.VT:
                        if VT_symbol in self.FollowSet[project_sentence[0]]:
                            print(self.FollowSet)
                            self.action[Ik_set][self.VT.index(VT_symbol)][0] = 'r'
                            # 获取产生式编号
                            item_num = 0
                            for i in range(len(self.lr0.grammarManager.sentences)):
                                if project_sentence[0] in self.lr0.grammarManager.sentences[i] and \
                                        project_sentence[1] in self.lr0.grammarManager.sentences[i]:
                                    item_num = i
                            self.action[Ik_set][self.VT.index(VT_symbol)][1] = item_num
                            continue
                # 条件3:S'->S·属于Ik
                if self.lr0.grammarManager.sentences[0][0] in project_sentence[0] and project_sentence[2] == 1:
                    self.action[Ik_set][self.VT.index('#')][0] = 'acc'
                    self.action[Ik_set][self.VT.index('#')][1] = -1
        # 条件4：直接遍历状态转移字典
        for go_key in self.lr0.translationArray.keys():
            if go_key[1] in self.VN:
                self.goto[go_key[0]][self.VN.index(go_key[1])] = self.lr0.translationArray[go_key]






if __name__ == '__main__':
    test_sentence = ["S'->E", "E->E+T", "E->T", "T->T*F", "T->F", "F->(E)", "F->i"]
    slr_table = SLRTable(test_sentence)
    slr_table.get_SLR_analysis_table()
    print(slr_table.action)
    print(slr_table.goto)
    print('action')
    for i in slr_table.action:
        print(i)
    print('goto')
    for j in slr_table.goto:
        print(j)
    print(slr_table.VN)
    print(len(slr_table.goto[0]))
    print('状态转移矩阵')
    print(slr_table.lr0.translationArray)
    for i in slr_table.lr0.states:
        print(i)
    print(len(slr_table.lr0.states))
    print(slr_table.lr0.grammarManager.sentences)
    print('follow元素')
    print(slr_table.FollowSet)
