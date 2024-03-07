from pyglet import text as pgtext
from pyglet.graphics import Group

from Code.Util.Settings import Settings


class Text:
    _text = Group(order=Settings.GroupOrderText)

    def __init__(self, text, x, y, batch):
        self.text = str(text)
        self.label = pgtext.Label(
            self.text, x=x, y=y, anchor_x='center', anchor_y='baseline', batch=batch, group=self._text,
            font_size=Settings.FontSize, color=(255, 255, 255, 255))
        self.x_offset, self.y_offset = 0, 0

    def remove(self):
        self.label.delete()

    def set_text(self, text):
        text = str(text)
        self.label.text = text

    def set_visible(self, visible):
        if visible:
            self.set_text(self.text)
        else:
            self.set_text("")

    def set_parent(self, parent):
        self.parent = parent

    def set_position(self, x, y):
        self.label.x, self.label.y = x, y

    def move(self, dx, dy):
        pass

    def update(self, dt):
        if self.parent:
            dx, dy = self.x_offset, self.y_offset
            dx += self.parent.sprite.width//2
            dy += self.parent.sprite.height
            x, y = self.parent.sprite.x, self.parent.sprite.y
            self.set_position(x+dx, y+dy)
