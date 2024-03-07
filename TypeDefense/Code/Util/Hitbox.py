from Code.Game import Game  # circular import, fix at some point


# default rectangle hitbox
class Hitbox:
    def __init__(self, obj):
        self.obj = obj
        self.groups = set()
        self.solid = True
        scale = Game.scale
        self.width, self.height = self.obj.sprite.width/scale, self.obj.sprite.height/scale

    def get_dimensions(self):
        return self.width, self.height

    def get_position(self):
        return self.obj.x, self.obj.y

    def collides(self, obj):
        x0, y0 = self.get_position()
        x1, y1 = obj.get_position()
        w0, h0 = self.get_dimensions()
        w1, h1 = obj.get_dimensions()

        return ((x1 < x0 < x1 + w1) or (x0 < x1 < x0 + w0)) and ((y1 < y0 < y1 + h1) or (y0 < y1 < y0 + h0))
