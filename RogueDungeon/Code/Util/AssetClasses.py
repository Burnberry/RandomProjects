from abc import ABC, abstractmethod
from pyglet import image, gl


class Asset(ABC):
    def __init__(self, name, path, extension):
        self.name, self.path, self.extension = name, path, extension
        self.n_loads = 0
        self.asset = None

    @abstractmethod
    def _load(self):
        pass

    def _unload(self):
        self.asset = None

    def release(self):
        self.n_loads -= 1
        if self.n_loads <= 0:
            self._unload()

    def get(self):
        self.n_loads += 1

        if self.asset is not None:
            return self.asset

        return self._load()

    def getPath(self):
        return self.path + self.name + '.' + self.extension


class ImageAsset(Asset):
    def __init__(self, name, path, extension="png"):
        super().__init__(name, path, extension)

    def _load(self):
        img = image.load(self.getPath())

        # Make sure to maintain pixelation in sprites
        texture = img.get_texture()
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        self.asset = img
        return img

    def getDimensions(self):
        """
        must be loaded
        return width, height
        """
        if not self.asset:
            print("asset is not loaded, can't get dimensions")
            return
        return self.asset.width, self.asset.height
