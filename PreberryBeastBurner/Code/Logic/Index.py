class Index:
    # Indexes added on top
    # Paths added at the bottom
    class Creature:
        player = 0
        rat = 1
        bat = 2
        spider = 3
        wolf = 4

    class Tile:
        _tile_offset = 1 * 2 ** 24
        grass = _tile_offset + 0
        rock = _tile_offset + 1

    class Overlay:
        _Overlay_offset = 2 * 2 ** 24
        tile_overlay_white = _Overlay_offset + 0

    filepath = {}
    _creature_path = "Assets/Creatures/"
    _tile_path = "Assets/Tiles/"
    _overlay_path = "Assets/Overlay/"
    _extension = ".png"

    filepath[Creature.player] = _creature_path + "Player" + _extension
    filepath[Creature.rat] = _creature_path + "Rat" + _extension
    filepath[Creature.bat] = _creature_path + "Bat" + _extension
    filepath[Creature.spider] = _creature_path + "Spider" + _extension
    filepath[Creature.wolf] = _creature_path + "Wolf" + _extension

    filepath[Tile.grass] = _tile_path + "Grass" + _extension
    filepath[Tile.rock] = _tile_path + "Rock" + _extension

    filepath[Overlay.tile_overlay_white] = _overlay_path + "tileOverlayWhite" + _extension
