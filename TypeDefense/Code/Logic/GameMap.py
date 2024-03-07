from Code.Util.TileGrid import TileGrid
from Code.Util import Assets


class GameMap(TileGrid):
    def __init__(self, paths, plots, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.paths = paths
        self.plots = plots

        for path in self.paths:
            positions = path.get_positions()
            for x, y in positions:
                if self.in_grid(x, y):
                    tile = self.get_tile(x, y)
                    tile.update_tile(Assets.Tile.Road, tile, tile.path)

        for plot in plots:
            x, y = plot.get_position()
            if self.in_grid(x, y):
                tile = self.get_tile(x, y)
                tile.update_tile(plot.asset, plot)
