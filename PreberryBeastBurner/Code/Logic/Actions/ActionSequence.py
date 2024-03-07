class ActionSequence:
    def __init__(self, actions):
        self.tag = None
        if len(actions) > 0:
            self.tag = actions[0].tag
        self.actions = actions

    def add_action(self, action):
        self.actions.append(action)
