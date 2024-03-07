from numpy.random import shuffle


class LineSet:
    lines: list

    def __init__(self, lines):
        self.load_lines(lines)
        self.used_lines = []

    def next_line(self, active_set):
        new_line = False
        while len(self.lines) > 0:
            line = self.lines.pop(0)
            self.used_lines.append(line)
            if line not in active_set:
                new_line = line
                break
        self.shuffle()
        return new_line

    def shuffle(self):
        if len(self.used_lines) >= len(self.lines):
            shuffle(self.used_lines)
            self.lines += self.used_lines
            self.used_lines = []

    def load_lines(self, lines):
        self.lines = lines
        shuffle(self.lines)
