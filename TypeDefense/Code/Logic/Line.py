class Line:
    activeLines = []

    def __init__(self, line, parent):
        self.parent = parent
        self.line = line
        self.activeLines.append(self)

    def hit(self):
        self.parent.hit()
        self.remove()

    def remove(self):
        if self in self.activeLines:
            self.activeLines.remove(self)

    @staticmethod
    def reset():
        Line.activeLines = []

    @staticmethod
    def submit_line(submitted_line):
        hits = []
        for line in Line.activeLines:
            if line.line == submitted_line:
                line.hit()
                hits.append(line)
        return hits
