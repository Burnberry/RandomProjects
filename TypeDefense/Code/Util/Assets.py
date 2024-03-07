from pyglet import image, gl, media

from Code.Util.Iter import Iter


_n_loaded = dict()
_loaded_assets = dict()

_filepath = {}
_creature_path = "Assets/Creatures/"
_tile_path = "Assets/Tiles/"
_overlay_path = "Assets/UI/"
_projectile_path = "Assets/Projectiles/"
_tower_path = "Assets/Towers/"
_sound_path = "Assets/Sounds/"
_extension = ".png"
_sound_extension = ".wav"


def add_asset(name, source):
    key = Iter.i()
    if source == "sound":
        path = _sound_path + name + _sound_extension
    elif source == "creature":
        path = _creature_path + name + _extension
    elif source == "tile":
        path = _tile_path + name + _extension
    elif source == "overlay":
        path = _overlay_path + name + _extension
    elif source == "projectile":
        path = _projectile_path + name + _extension
    elif source == "tower":
        path = _tower_path + name + _extension
    else:
        print("Error, Asset type not recognized")
        return

    _filepath[key] = path
    return key


def get_asset(index):
    if _n_loaded.get(index, 0) > 0:
        _n_loaded[index] += 1
        return _loaded_assets[index]
    else:
        img = image.load(_filepath[index])

        # Make sure to maintain pixelation in sprites
        texture = img.get_texture()
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        _loaded_assets[index] = img
        _n_loaded[index] = 1
        return img


def get_sound(index):
    if _n_loaded.get(index, 0) > 0:
        _n_loaded[index] += 1
        return _loaded_assets[index]
    else:
        sound = media.StaticSource(media.load(_filepath[index]))

        _loaded_assets[index] = sound
        _n_loaded[index] = 1
        return sound


def release_asset(self, index):
    self._n_loaded[index] -= 1
    if self._n_loaded[index] == 0:
        self._loaded_assets[index] = None


# Indexes added on top
# Paths added at the bottom


class Creature:
    Player = add_asset("Player", "creature")
    Peasant0 = add_asset("Peasant0", "creature")
    Peasant1 = add_asset("Peasant1", "creature")
    Bat = add_asset("Bat", "creature")
    Castle = add_asset("Castle", "creature")


class Tower:
    TowerDefault = add_asset("TowerDefault", "tower")


class Projectile:
    BallElemental = add_asset("BallElemental", "projectile")


class Sound:
    Knock = add_asset("Knock", "sound")
    Key = add_asset("Key", "sound")
    Enter = add_asset("Enter", "sound")


class Tile:
    Grass = add_asset("Grass", "tile")
    Road = add_asset("Road", "tile")


class Overlay:
    tileOverlay = add_asset("tileOverlay", "overlay")
