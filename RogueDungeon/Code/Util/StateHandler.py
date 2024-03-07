class StateHandler:
    """
    Keeps track of a state and which objects get to act in chain of command
    Objects must have updateState(dt, state) implemented
    """
    def __init__(self, subject, state):
        self.setState(subject, state)
        self.chain = []

    def update(self, dt):
        self.subject.updateState(dt, self.state)

    def interrupt(self, subject, state):
        self.AddToChain()
        self.setState(subject, state)

    def AddToChain(self):
        self.chain.append((self.subject, self.state))

    def release(self):
        self.setState(*self.chain.pop())

    def setState(self, subject, state):
        self.subject, self.state = subject, state

    def isState(self, state):
        return state == self.state

    def isSubject(self, subject):
        return subject is self.subject

    def isActive(self, subject, state):
        return self.isState(state) and self.isSubject(subject)
