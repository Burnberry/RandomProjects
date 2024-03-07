from Code.Util.GameObject import GameObject
from Code.Util.Tile import Tile
from Code.Util import Assets


class TileGrid:
    def __init__(self, batch, camera, w, h, w0=0, h0=0, dw=0, dh=0):
        self.batch = batch
        self.camera = camera
        self.w, self.w0, self.h, self.h0 = w, w0, h, h0
        self.dw, self.dh = dw, dh
        self.grid = [[self.make_tile(x, y) for x in range(w0, w)] for y in range(h0, h)]

    def make_tile(self, x, y, asset=Assets.Tile.Grass):
        x += self.dw
        y += self.dh
        if asset == Assets.Tile.Road:
            print(x, y)
        group = GameObject.Background
        obj = GameObject(asset, self.batch, self.camera, x, y, center=True, group=group)
        tile = Tile(obj, asset)
        return tile

    def get_tile(self, x, y):
        if self.in_grid(x, y):
            x -= self.w0
            y -= self.h0
            return self.grid[y][x]

    def in_grid(self, x, y):
        return self.w0 <= x+self.dw <= self.w and self.h0 <= y+self.dh <= self.h
