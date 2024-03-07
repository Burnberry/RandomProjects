class Animator:
    def __init__(self, obj, indexes, delay):
        self.obj = obj
        self.indexes = indexes
        self.current_index = self.indexes[0]
        self.delay = delay
        self.time_left = delay

        self.obj.add_updatable(self)

    def update(self, dt):
        self.time_left -= dt

        if self.time_left <= 0:
            self.time_left += self.delay
            self.next_asset()

    def next_asset(self):
        i = self.indexes.index(self.current_index) + 1
        if i >= len(self.indexes):
            i -= len(self.indexes)
        self.current_index = self.indexes[i]
        self.obj.use_asset(self.current_index)
