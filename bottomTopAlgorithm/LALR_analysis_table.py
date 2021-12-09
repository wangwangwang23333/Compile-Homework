from bottomTopAlgorithm.LRk_state_transfer_generation import LR1
from bottomTopAlgorithm.action import Action
import copy


class LALRTable:
    """
    LALR 分析表产生类，有以下几个步骤：
    1, 对于 LR1 算法产生的状态 DFA，合并同类项，并且改变 transfer_array 矩阵
    2, 产生分析表
    """

    def __init__(self, lr1: LR1):
        self.lr1 = lr1
        self.lr1.calculateDFA()
        self.lr1_state_transfer_array = self.lr1.get_numbered_and_looking_forward_transfer_array()
        self.lr1_states = self.lr1.get_merged_looking_forward_string()
        self.states = []
        self.state_transfer_array = dict()
        self.action = dict()
        self.goto = dict()
        self.reduce_states()
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

    def reduce_states(self):
        """
        按照 LALR 的要求缩减状态数量并且产生新的 states
        :return: 新的 DFA states
        """
        new_states = []
        # 记录下合并的项
        reduce_set = set()
        reduce_list_state = copy.deepcopy(self.lr1_states)
        transfer_array = copy.deepcopy(self.lr1_state_transfer_array)
        for index_i, i in enumerate(reduce_list_state):
            if index_i in reduce_set:
                continue
            merge_flag = False
            for index_j, j in enumerate(reduce_list_state):
                # 跳过本身相同的项和已经被排除的项
                if i == j or index_j in reduce_set:
                    continue
                if LALRTable._compare_state_discarding_lft(i, j):
                    # i j 是相同的状态，只是展望符不同。
                    new_states.append(LALRTable._merge_two_states(i, j))
                    reduce_set.add(index_j)
                    for state_i, v in self.lr1_state_transfer_array.items():
                        if v == index_j:
                            transfer_array[state_i] = index_i
                    merge_flag = True
            if not merge_flag:
                new_states.append(i)
        self.get_LALR_transfer_array(reduce_set, transfer_array)
        self.states = new_states
        return new_states

    def get_LALR_transfer_array(self, reduce_set, transfer_array):
        """
        通过新的状态和状态转移矩阵计算得出一个 LALR 分析表
        :param reduce_set: 去掉的状态
        :param transfer_array: 之前的状态转移矩阵
        :return: 新的状态转移矩阵
        """
        # 原始状态数
        old_state_num = len(self.lr1_states)
        # 刚刚被合并的状态要移除
        remove_list = []
        for i in reduce_set:
            for j in transfer_array.keys():
                if j[0] == i:
                    remove_list.append(j)

        # 从 transfer_array 中移除
        for i in remove_list:
            transfer_array.pop(i)

        # 状态下标有改变，用一个 dict 记录改变前后
        change_map = {i: i for i in range(old_state_num)}

        for i in reduce_set:
            for v in change_map.keys():
                if v > i:
                    change_map[v] -= 1

        # 这些状态移除之后才能给 new_array 赋值
        filter_set = set()
        for k, v in change_map.items():
            if k != v:
                filter_set.add(k)

        # 再做一次移除
        remove_list = []
        for i in filter_set:
            for j in transfer_array.keys():
                if j[0] == i:
                    remove_list.append(j)

        # 终于填充了 new_array 并且排除了不要的元素
        new_array = copy.deepcopy(transfer_array)
        for i in remove_list:
            new_array.pop(i)

        # 用状态下标的变化来做新的填充
        for pos, v in transfer_array.items():
            if type(v) is int:
                new_array[(change_map[pos[0]], pos[1])] = change_map[v]
            else:
                new_array[(change_map[pos[0]], pos[1])] = v
        # 赋值给 self 变量，完成初始化
        self.state_transfer_array = new_array
        # print(new_array)
        return new_array

    @staticmethod
    def _merge_two_states(state1, state2):
        new_state = []
        for state_item1 in state1:
            state_item_merged = copy.deepcopy(state_item1[:3])
            for state_item2 in state2:
                if state_item1[:3] == state_item2[:3]:
                    lft = list(set(state_item1[3]).union(set(state_item2[3])))
                    state_item_merged.append(lft)
                    if len(state_item1) == 5:
                        state_item_merged.append(state_item1[4])
                    if len(state_item2) == 5:
                        state_item_merged.append(state_item2[4])
            new_state.append(state_item_merged)
        return new_state

    @staticmethod
    def _compare_state_discarding_lft(state1, state2):
        set1 = LALRTable._get_set_from_state(state1)
        set2 = LALRTable._get_set_from_state(state2)
        return set1 == set2

    @staticmethod
    def _get_set_from_state(state):
        return {(i[0], i[1], i[2]) for i in state}

    def get_analysis_table(self):
        """
        返回 LALR 算法分析表。
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
        rows = len(self.states)
        table = []

        nVT = len(self.table_VT)
        nVN = len(self.table_VN)
        # 生成全是 '' 的表
        for i in range(rows + 1):
            table.append([''] * (nVT + nVN + 1))
        # 第一列是序号
        for i in range(1, rows + 1):
            table[i][0] = i - 1
        # 第一行是符号
        for i in range(nVN + nVT):
            if i < nVT:
                table[0][i + 1] = self.table_VT[i]
            else:
                table[0][i + 1] = self.table_VN[i - nVT]
        for pos, item in self.action.items():
            table[pos[0] + 1][self._get_index_of_v(pos[1])] = item
        for pos, item in self.goto.items():
            table[pos[0] + 1][self._get_index_of_v(pos[1])] = item

        return table

    def show(self):
        """
        打印出来
        :return: None
        """
        for i in self.get_visible_table():
            for j in i:
                if j !='':
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

    def getStateStr(self,index):
        # 输出states[index]的字符串
        return


        item=self.states[index]
        # 对item合并状态
        newItem = []
        curItem = copy.deepcopy(item)
        item = copy.deepcopy(item)
        while len(item) > 0:
            result = []
            basicLine = [item[0][0], item[0][1], item[0][2]]
            for i in curItem:
                if i[0] == basicLine[0] and i[1] == basicLine[1] and i[2] == basicLine[2]:
                    # 将item.index(i)移除
                    result.append(i[3])
                    item.remove(i)

            # 排序，按照字母顺序输出，这样好看
            result.sort()

            # 将item整理成一个字符串
            preStr = ""
            for kindex, kitem in enumerate(result):
                if kindex != 0:
                    preStr += "|"
                preStr += kitem
            
            newItem.append([basicLine[0], basicLine[1], basicLine[2], preStr])

        showLabel = ""
        # str(index)+"     "
        for jndex,j in enumerate(newItem):

            if jndex!=0:
                showLabel += "\n"

            showLabel += j[0] + "->"
            for t in range(len(j[1])):
                if t == j[2]:
                    showLabel += "·"
                showLabel += j[1][t]
            if j[2] >= len(j[1]):
                showLabel += "·"

            showLabel += "," + j[3]

            
        
        return showLabel

if __name__ == "__main__":
    lr1 = LR1()
    lr1.grammarManager.getInput()
    table = LALRTable(lr1)
    table.show()
