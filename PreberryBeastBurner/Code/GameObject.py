from pyglet import sprite


class GameObject:
    def __init__(self, loaded_image, batch, group, scale=1, x=0, y=0, dx=0, dy=0, alpha=255, inst=None):
        self.sprite = sprite.Sprite(loaded_image, batch=batch, group=group)
        self.sprite.opacity = alpha
        # self.sprite.scale = scale
        self.color = (0, 0, 0)

        self.dx, self.dy = dx * scale, dy * scale
        self.set_position(x, y)

        # For buttons
        self.instruction = inst

    def set_position(self, x, y):
        self.sprite.x = x + self.dx
        self.sprite.y = y + self.dy

    def remove(self):
        self.sprite.delete()