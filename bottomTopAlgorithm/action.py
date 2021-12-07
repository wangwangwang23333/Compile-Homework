class Action:
    """
    对应 Action 表中的 action
    """

    def __init__(self, state, act="shift"):
        self.state = state
        self.action = act
        if not self.action.startswith("s") and not self.action.startswith("r") and not self.action.startswith("a"):
            raise Exception("没有这样的动作" + act)
        if self.action.startswith("a"):
            self.state = -1

    def __repr__(self):
        if self.action.startswith("a"):
            return "acc"
        return self.action[0] + str(self.state)
