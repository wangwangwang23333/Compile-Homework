from bottomTopAlgorithm.GrammarManager import GrammarManager
import copy


# 想用这种办法重构代码，这样比较可拓展
class StateItem:
    """
    一个 LR1 DFA 当中的产生式状态，有很多个属性：
    1. 产生式左部
    2. 产生式右部
    3. 当前接受位置
    4. 当前状态式接受字符
    5. 规约所属表达式编号
    6. 展望符
    """

    def __init__(self, left, right, pos, acc, no=None, looking=None):
        self.left_side = left
        self.right_side = right
        self.position = pos
        self.accept = acc
        self.number = no
        self.looking_forward = looking
        if len(self.right_side) <= self.position:
            raise Exception("接受位错误，超出产生式本身")

    def __str__(self):
        s = ""
        s += self.left_side
        s += '->' + self.right_side[0:self.position] + '·' + self.right_side[self.position:len(self.right_side)]
        s += ", " + self.accept
        s += "; " + "(No. " + str(self.number) + "; "
        for i in self.looking_forward:
            s += i + ', '
        s += ')'
        return s

    def __repr__(self):
        return str(self)


class LR1LookingForward:
    """
    从汪明杰的文件里 Copy 过来的。
    TODO： 在 state_transfer_array 中添加 No. 和 展望符
    """

    def __init__(self):
        self.state_transfer_array = dict()
        self.states = dict()
        self.grammarManager = GrammarManager()
        self.grammarManager.getInput()

    def get_closure(self, initial_relation):
        """
        计算initialRelation的闭包
        """
        result = [initial_relation]

        # 闭包中的数量是否增加
        new_appear = True
        while new_appear:
            new_appear = False

            for res in result:
                # 获取.右边的符号
                if res[2] >= len(res[1]):
                    continue
                right_symbol = res[1][res[2]]

                # 查看是否有该产生式 right_symbol-> xxx
                for i in range(len(self.grammarManager.sentences)):
                    if self.grammarManager.sentences[i][0] == right_symbol:
                        # right_symbol-> self.grammarManager.sentences[i][1]
                        # 接下来是确定 First(beta a),其中beta为再下一个字符
                        initial_first = ""
                        if res[2] + 1 < len(res[1]):
                            initial_first += res[1][res[2] + 1]
                        initial_first += res[3]  # res[3]为预测符
                        print("initialFirst为", initial_first)
                        # 计算First(initial_first)
                        first_result_set = self.grammarManager.getFirstSet(initial_first)

                        print("firstResultSet为", first_result_set)

                        # firstSet中的终结符
                        for vt in first_result_set:
                            # 如果不是终结符或者#，则不考虑
                            if not (vt in self.grammarManager.VT or vt == '#'):
                                continue

                            # 是终结符，则查看该结果是否已经出现过
                            newRes = [right_symbol, self.grammarManager.sentences[i][1], 0, vt]

                            if not newRes in result:
                                result.append(newRes)
                                new_appear = True
        return result

    def get_go_IX(self, I, X):
        """
        计算Go(I,X):即在状态I下接受输入X
        """
        result = []
        for i in I:
            if i[2] >= len(i[1]):
                continue
            # 下一个字符
            if i[1][i[2]] == X:
                if not [i[0], i[1], i[2] + 1, i[3]] in result:
                    result.append([i[0], i[1], i[2] + 1, i[3]])
        # 对result中每一个表达式计算闭包
        new_result = result
        for i in result:
            tempResults = self.get_closure(i)
            # 对于tempResults中的每一个元素
            for j in tempResults:
                if not j in result:
                    new_result.append(j)
        return new_result

    def calculate_DFA(self):
        """
        计算DFA
        """
        # 每一个状态闭包，应当是一个集合
        initial_relation = [self.grammarManager.sentences[0][0],
                            self.grammarManager.sentences[0][1], 0, '#']
        initial_state = self.get_closure(initial_relation)

        self.states = [initial_state]

        # 从initialState开始扩展
        has_grown = True
        while has_grown:
            has_grown = False
            newStates = copy.deepcopy(self.states)

            for i, item in enumerate(self.states):

                # 遍历终结符
                for j in self.grammarManager.VT:

                    new_state = self.get_go_IX(item, j)

                    # 为空，则表示不可以接受该符号
                    if new_state == []:
                        continue

                    # 判断新状态是否已经存在
                    if new_state in newStates:
                        # 获取newState下标
                        new_state_index = newStates.index(new_state)

                        # 填充状态转移矩阵
                        self.state_transfer_array[(i, j)] = new_state_index
                    else:
                        # 加入新状态
                        newStates.append(new_state)
                        has_grown = True

                        # 填充状态转移矩阵
                        self.state_transfer_array[(i, j)] = len(newStates) - 1

                # 遍历非终结符
                for j in self.grammarManager.VN:

                    new_state = self.get_go_IX(item, j)

                    # 为空，则表示不可以接受该符号
                    if new_state == []:
                        continue

                    # 判断新状态是否已经存在
                    if new_state in newStates:
                        # 获取newState下标
                        new_state_index = newStates.index(new_state)

                        # 填充状态转移矩阵
                        self.state_transfer_array[(i, j)] = new_state_index
                    else:
                        # 加入新状态
                        newStates.append(new_state)
                        has_grown = True

                        # 填充状态转移矩阵
                        self.state_transfer_array[(i, j)] = len(newStates) - 1

            self.states = newStates


class LR1Table:

    def __init__(self):
        self.lr1 = LR1LookingForward()


if __name__ == "__main__":
    s = StateItem("E'", "E", 1, "#", 3, ['#', '&'])
    print(s)