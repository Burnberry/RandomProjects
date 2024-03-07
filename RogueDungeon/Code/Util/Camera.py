class Camera:
    def __init__(self, x, y, screen_width, screen_height, offset):
        self.screenWidth, self.screenHeight = screen_width, screen_height
        self.offset = offset
        self.x, self.y = x, y
        self.w, self.h = screen_width//offset, screen_height//offset

    def isOnScreen(self, x, y, w=0, h=0):
        xcheck = self.x < x+w and self.x+self.w > x
        ycheck = self.y < y+h and self.y+self.h > y
        return xcheck and ycheck

    def screenToGameCoords(self, cx, cy):
        return self.x + cx/self.offset, self.y + cy/self.offset

    def gameToScreenCoords(self, x, y):
        return (x - self.x)*self.offset, (y - self.y)*self.offset

    def setLocation(self, x, y):
        self.x, self.y = x, y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def getCenter(self):
        x, y = self.x + self.w/2, self.y + self.h/2
        return x, y

    def getScreenCenter(self):
        return self.screenWidth//2, self.screenHeight//2

    def getScreenPosition(self, anchor):
        w, h = self.screenWidth, self.screenHeight
        cx, cy = 0, 0
        ax, ay = anchor[1], anchor[0]
        if ax == 'c':
            cx = w // 2
        elif ax == 'r':
            cx = w - 1

        if ay == 'c':
            cy = h // 2
        elif ay == 't':
            cy = h - 1

        return cx, cy
