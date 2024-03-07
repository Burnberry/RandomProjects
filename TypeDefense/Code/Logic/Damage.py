from Code.Util.Iter import Iter


class Damage:
    Projectile = Iter.i()

    def __init__(self, source, target, value, method):
        self.source = source
        self.target = target
        self.value = value
        self.method = method


