class Iter:
    n = 0

    @staticmethod
    def i():
        n = Iter.n
        Iter.n += 1
        return n
