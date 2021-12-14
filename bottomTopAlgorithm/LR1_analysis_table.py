"""
@author zzy
@date
"""
from bottomTopAlgorithm.LRk_state_transfer_generation import LR1
from bottomTopAlgorithm.action import Action
import copy


class LR1Table:
    """
    LR1 分析表构造类
    通过
    """

    def __init__(self, lr1):
        self.lr1 = lr1
        self.lr1.calculateDFA()
        self.state_transfer_array = self.lr1.get_numbered_and_looking_forward_transfer_array()
        self.states = self.lr1.get_merged_looking_forward_string()
        self.action = dict()
        self.goto = dict()
        self.get_analysis_table()

        # 为了打印表格的变量
        self.table_VN = copy.deepcopy(self.lr1.grammarManager.VN)
        self.table_VT = copy.deepcopy(self.lr1.grammarManager.VT)
        # VT 含有 #
        self.table_VT.append("#")
        # 跳过 S'
        for i in self.table_VN:
            if len(i) > 1:
                self.table_VN.remove(i)

    def get_analysis_table(self):
        """
        返回LR(1) 算法分析表。
        一个元组，(action表, goto表)
        :return: (action表, goto表)
        """
        for pos, state in self.state_transfer_array.items():
            if len(pos[1]) > 1 and pos[1][1] == "'":
                self.action[pos] = Action(0, 'acc')
            elif pos[1] in self.lr1.grammarManager.VT:
                self.action[pos] = Action(state, "shift")
            elif pos[1] in self.lr1.grammarManager.VN:
                self.goto[pos] = state
            elif pos[1] == "no":
                row = pos[0]
                lft = self.state_transfer_array[(row, "lft")]
                for s in lft:
                    if len(self.lr1.grammarManager.sentences[state][0]) == 1:
                        self.action[(row, s)] = Action(state, "reduce")
                    else:
                        self.action[(row, s)] = Action(0, "acc")
        return self.action, self.goto

    def get_visible_table(self):
        """
        把 dict 转化成跟题中一样的表格，存在 list 里
        :return: 一个二维数组
        """
        rows = len(self.lr1.get_merged_looking_forward_string())
        table = []

        nVT = len(self.table_VT)
        nVN = len(self.table_VN)
        # 生成全是 '' 的表
        for i in range(rows+1):
            table.append(['']*(nVT + nVN + 1))
        # 第一列是序号
        for i in range(1, rows+1):
            table[i][0] = i-1
        # 第一行是符号
        for i in range(nVN + nVT):
            if i < nVT:
                table[0][i+1] = self.table_VT[i]
            else:
                table[0][i+1] = self.table_VN[i-nVT]
        for pos, item in self.action.items():
            table[pos[0]+1][self._get_index_of_v(pos[1])] = item
        for pos, item in self.goto.items():
            table[pos[0]+1][self._get_index_of_v(pos[1])] = item

        return table

    def show(self):
        """
        打印出来
        :return: None
        """
        for i in self.get_visible_table():
            for j in i:
                if j != '':
                    print(j, '\t', end="")
                else:
                    print('\t', end="")
            print()

    def _get_index_of_v(self, v):
        """
        就是要转化数组的时候用的私有函数。
        :param v: 一个符号
        :return: 这个符号所在的表格中的列
        """
        if v.isupper():
            return self.table_VN.index(v) + len(self.table_VT) + 1
        return self.table_VT.index(v) + 1

    def get_state_str(self, index):
        # 输出states[index]的字符串

        item = self.states[index]
        showLabel = ""
        # str(index)+"     "
        for jndex, j in enumerate(item):
            if jndex != 0:
                showLabel += "\n"
            showLabel += j[0] + "->"
            for t in range(len(j[1])):
                if t == j[2]:
                    showLabel += "·"
                showLabel += j[1][t]
            if j[2] >= len(j[1]):
                showLabel += "·"
            showLabel += ","
            lfts = copy.deepcopy(j[3])
            lfts.sort()
            for index_lft, lft in enumerate(lfts):
                if index_lft != 0:
                    showLabel += '|'
                showLabel += lft
            if len(j) == 5:
                showLabel += "[" + str(j[4]) + ']'
        return showLabel


"""
测试：
4
S'->S
S->BB
B->aB
B->b

3
E'->E
E->(E)
E->i
"""
if __name__ == "__main__":
    lr1 = LR1()
    lr1.grammarManager.getInput()
    table = LR1Table(lr1)
    table.show()
    for i in range(len(table.states)):
        print("State", str(i) + ":")
        print(table.get_state_str(i))
        print()
