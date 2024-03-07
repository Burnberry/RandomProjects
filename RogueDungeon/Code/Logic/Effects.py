from Code.Util.Assets import Img
from Code.Util.GameObject import TextGameObject, SpriteGameObject


class Effect:
    def __init__(self, parent, gameObject, x=0, y=0, ttl=1.0, speed=0, direction=(0, 1)):
        self.parent = parent
        self.gameObject = gameObject
        self.ttl = ttl
        self.x, self.y = x, y
        self.speed = speed
        self.setDirection(*direction)
        self.updateVector()
        self.updatePosition()

        self.parent.addEffect(self)

    def update(self, dt):
        self.ttl -= dt
        if self.ttl <= 0:
            self.remove()

        dx, dy = self.moveVector
        self.x += dx*dt
        self.y += dy * dt
        self.updatePosition()

    def updatePosition(self):
        x, y = self.parent.getPosition()
        x, y = x + self.x, y + self.y
        self.gameObject.setPosition(x, y)

    def remove(self):
        self.parent.removeEffect(self)
        self.gameObject.remove()

    def setSpeed(self, speed):
        self.speed = speed
        self.updateVector()

    def setDirection(self, x, y):
        mag = (x**2 + y**2)**0.5
        x, y = x/mag, y/mag
        self.direction = (x, y)
        self.updateVector()

    def updateVector(self):
        x, y = self.direction
        self.moveVector = (x*self.speed, y*self.speed)


class FloatingText(Effect):
    def __init__(self, parent, text, color=(160, 10, 30), ttl=1, scale=1, speed=20):
        text = str(text)
        x, y = parent.getAnchoredPosition("tc")
        dx, dy = parent.getPosition()
        gameObject = TextGameObject(parent.scene, 0, 0, parent.Group.Text, "bc", text, scale)
        gameObject.setColor(color)
        direction = (0, 1)
        super().__init__(parent, gameObject, x-dx, y-dy, ttl, speed, direction)


class GenericSingle(Effect):
    def __init__(self, parent, delay=0.0, anchor="tc", img=Img.Stack, color=None):
        self.delay = delay
        x, y = parent.getAnchoredPosition(anchor)
        dx, dy = parent.getPosition()
        gameObject = SpriteGameObject(parent.scene, 0, 0, SpriteGameObject.Group.UI, anchor, img)
        if color is not None:
            gameObject.setColor(color)
        if delay > 0:
            gameObject.deactivate()
        ttl = 0.8
        speed = 10
        direction = (0, -1)
        super().__init__(parent, gameObject, (x-dx)*0.75, y-dy, ttl, speed, direction)

    def update(self, dt):
        if self.delay >= 0:
            self.delay -= dt
            if self.delay < 0:
                self.gameObject.activate()
                super().update(-self.delay)
        else:
            super().update(dt)


class Poison:
    def __init__(self, parent):
        for delay, anchor in [(0.0, "tc"), (0.25, "tr"), (0.5, "tl")]:
            effect = GenericSingle(parent, delay, anchor, Img.StackPoison)


class GenericEffect:
    def __init__(self, parent, img, color=None):
        for delay, anchor in [(0.0, "tc"), (0.25, "tr"), (0.5, "tl")]:
            effect = GenericSingle(parent, delay, anchor, img, color)
