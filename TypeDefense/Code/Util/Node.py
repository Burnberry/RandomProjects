class Node:
    def __init__(self, position):
        self.position = position
        self.parent = None
        self.child = None

    def chain(self, parent):
        if self.parent:
            self.parent.child = None
        self.parent = parent
        self.parent.child = self
