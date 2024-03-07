import pyglet.libs.win32.constants


from pyglet.window import Window


# Allow alt tab while in fullscreen
pyglet.libs.win32.constants.HWND_TOPMOST = pyglet.libs.win32.constants.HWND_NOTOPMOST


class Camera:
    def __init__(self, x, y, screen_width, screen_height, offset, fullscreen=False):
        self.x, self.y = x, y
        self.w, self.h = screen_width//offset, screen_height//offset
        self.offset = offset

        self.screenWidth = screen_width
        self.screenHeight = screen_height

        if fullscreen:
            self.window = Window(fullscreen=fullscreen)
        else:
            self.window = Window(width=self.screenWidth, height=self.screenHeight)

    def inside(self, x, y):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    def to_game_coords(self, cx, cy):
        return self.x + cx/self.offset, self.y + cy/self.offset

    def to_screen_coords(self, x, y):
        return (x - self.x)*self.offset, (y - self.y)*self.offset

    def close(self):
        self.window.close()

    def dispatch_events(self):
        return self.window.dispatch_events()

    def set_location(self, x, y):
        self.x, self.y = x, y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def clear(self):
        self.window.clear()

    def flip(self):
        self.window.flip()

    def get_window(self):
        return self.window

    def get_center(self):
        x, y = self.x + self.w/2, self.y + self.h/2
        return x, y
