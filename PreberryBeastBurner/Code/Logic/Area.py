from random import randint

from Code.Logic.Index import Index


class Tile:
    def __init__(self, x, y, sprite=Index.Tile.grass):
        self.x, self.y = x, y
        if randint(0, 15) == 15:
            sprite = Index.Tile.rock
        self.sprite = sprite
        self.entity = None

    def getEntity(self):
        return self.entity

    def setEntity(self, entity):
        self.entity = entity

    def show(self):
        if self.entity: 
            return self.entity.show()
        else:
            return self.sprite


class Area:
    def __init__(self, width, height):
        self.field = [[Tile(x, y) for x in range(width)] for y in range(height)]
        self.width, self.height = width, height

    def getTile(self, x, y):
        return self.field[y][x]

    def setTile(self, x, y, tile):
        if self.field[y][x] is None:
            print("ERROR: Tile already occupied")
        else:
            self.field[y][x] = tile

    def inside_area(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
