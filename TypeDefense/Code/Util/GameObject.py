from pyglet import sprite, graphics

from Code.Util import Assets
from Code.Util.Settings import Settings
from Code.Util.Text import Text
from Code.Util.SoundPlayer import SoundPlayer
# from Code.Util.Hitbox import Hitbox # Needs fix


class GameObject:
    sprite: sprite
    # Set of all game objects
    objects = set()

    # different batches for rendering
    batch = graphics.Batch()

    soundPlayer = SoundPlayer(None)

    Background = graphics.Group(order=Settings.GroupOrderBackground)
    Foreground = graphics.Group(order=Settings.GroupOrderForeground)
    UI = graphics.Group(order=Settings.GroupOrderUI)

    @staticmethod
    def update_entities(dt):
        for obj in GameObject.objects.copy():
            if obj in GameObject.objects:
                obj.update(dt)

    def __init__(self, asset_index, batch, camera, x=0, y=0, alpha=255, visible=True, parent=None, center=True,
                 w_offset=0.5, h_offset=0.5, group=Foreground):
        self.camera = camera
        self.x, self.y = None, None
        self.center = center
        self.parent = parent
        self.children = []
        self.w_offset, self.h_offset = w_offset, h_offset

        self.assets_indexes = [asset_index]
        self.asset_index = asset_index
        self.sprite = sprite.Sprite(Assets.get_asset(self.asset_index), batch=batch, group=group)
        self.set_scale(Settings.Scale)
        self.set_position(x, y)
        self.set_alpha(alpha)
        self.tag = None
        self.set_visible(visible)

        GameObject.objects.add(self)

    def remove(self):
        self.objects.remove(self)
        self.sprite.delete()
        for obj in self.children:
            obj.remove()

    def set_position(self, x, y):
        if (x == self.x and y == self.y) or not self.sprite.visible:
            self.x, self.y = x, y
            return
        self.x, self.y = x, y

        cx, cy = self.camera.to_screen_coords(x, y)
        if self.center:
            cx -= self.sprite.width*self.w_offset
        # Could check here if on screen first, probably once hitbox is implemented
        self.sprite.x, self.sprite.y = cx, cy

    def get_position(self):
        return self.x, self.y

    def get_center(self):
        x, y = self.get_position()
        w, h = self.camera.to_game_coords(self.sprite.width * self.w_offset, self.sprite.height * self.h_offset)
        if not self.center:
            x += w
        y += h
        return x, y

    def move(self, dx, dy):
        x, y = self.x + dx, self.y + dy
        self.set_position(x, y)
        for child in self.children:
            child.move(dx, dy)

    def set_scale(self, scale):
        self.sprite.scale = scale

    def set_alpha(self, alpha):
        self.sprite.opacity = alpha

    def set_color(self, color):
        self.sprite.color = color

    def set_visible(self, visible):
        self.sprite.visible = visible
        if self.tag:
            self.tag.set_visible(visible)

    def set_tag(self, text):
        self.tag = text
        text.set_parent(self)
        self.children.append(self.tag)
        self.tag.update(0)

    def use_asset(self, index):
        self.asset_index = index
        self.sprite.image = Assets.get_asset(index)

    def update(self, dt):
        for obj in self.children:
            obj.update(dt)
