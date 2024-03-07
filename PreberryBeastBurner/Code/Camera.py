class Camera:
    def __init__(self, x, y, screen_width, screen_height, tile_offset):
        self.x, self.y = x, y
        self.w, self.h = screen_width//tile_offset, screen_height//tile_offset
        self.screenWidth = screen_width
        self.screenHeight = screen_height

    def inside(self, x, y):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h
