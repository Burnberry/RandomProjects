from Code.Util.Iter import Iter


class Tile:
    default = Iter.i()
    path = Iter.i()
    tower = Iter.i()

    def __init__(self, obj, tag, tile_type=default, child=None):
        self.obj = obj
        self.tag = tag
        self.tile_type = tile_type
        self.child = child

    def set_child(self, child):
        self.child = child

    def update_tile(self, asset, tag, tile_type=None):
        self.tag = tag
        self.obj.use_asset(asset)
        if tile_type:
            self.set_tile_type(tile_type)

    def set_tile_type(self, tile_type):
        self.tile_type = tile_type
