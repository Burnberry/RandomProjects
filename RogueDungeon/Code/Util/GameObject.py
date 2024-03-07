from abc import ABC, abstractmethod

from pyglet.shapes import Rectangle, Line
from pyglet.sprite import Sprite
from pyglet.text import Label as Label
from pyglet import graphics, image, gl

from Code.Util.SettingsGlobal import SettingsGlobal


class AbstractGameObject(ABC):
    activeObjects = set()
    _clearing = False

    batch = graphics.Batch()

    class Group:
        Background = graphics.Group(order=SettingsGlobal.GroupOrderBackground)
        Foreground = graphics.Group(order=SettingsGlobal.GroupOrderForeground)
        UI = graphics.Group(order=SettingsGlobal.GroupOrderUI)
        Text = graphics.Group(order=SettingsGlobal.GroupOrderText)
        TextBackground = graphics.Group(order=SettingsGlobal.GroupOrderTextBackground)
        TextDisplay = graphics.Group(order=SettingsGlobal.GroupOrderTextDisplay)
        TextDisplayBackground = graphics.Group(order=SettingsGlobal.GroupOrderTextDisplayBackground)
        Popup = graphics.Group(order=SettingsGlobal.GroupOrderPopup)
        PopupBackground = graphics.Group(order=SettingsGlobal.GroupOrderPopupBackground)

    @staticmethod
    def updateActiveObjects(dt):
        for obj in AbstractGameObject.activeObjects.copy():
            if obj in AbstractGameObject.activeObjects:
                obj.update(dt)

        for obj in AbstractGameObject.activeObjects:
            if isinstance(obj, AbstractGameVisualObject):
                obj.updateVisual()

    @staticmethod
    def clear():
        AbstractGameObject._clearing = True
        for obj in AbstractGameObject.activeObjects.copy():
            if obj in AbstractGameObject.activeObjects:
                obj.remove()
        AbstractGameObject._clearing = False

    def __init__(self):
        self.associatedObjects = set()

        AbstractGameObject.activeObjects.add(self)
        self.removed = False

    @abstractmethod
    def update(self, dt):
        pass

    def remove(self):
        if self in self.activeObjects:
            self.activeObjects.remove(self)

        for obj in self.associatedObjects:
            obj.signalAssociateRemoval(self)
        self.removed = True

    def addAssociate(self, obj):
        self.associatedObjects.add(obj)

    def removeAssociate(self, obj):
        if obj in self.associatedObjects:
            self.associatedObjects.remove(obj)

    def isRemoved(self):
        return self.removed


class AbstractGamePositionalObject(AbstractGameObject):
    def __init__(self, scene, x, y):
        super().__init__()
        self.scene = scene
        self.x, self.y = x, y

    @abstractmethod
    def update(self, dt):
        pass

    def getPosition(self):
        return self.x, self.y

    def getScreenPosition(self) -> (int, int):
        return self.scene.game.camera.gameToScreenCoords(*self.getPosition())

    def setPosition(self, x, y):
        self.x, self.y = x, y

    def activate(self):
        self.setActive(True)

    def deactivate(self):
        self.setActive(False)

    @abstractmethod
    def setActive(self, active):
        pass

    @abstractmethod
    def getScreenDimensions(self) -> (int, int):
        pass


class AbstractGameVisualObject(AbstractGamePositionalObject):
    def __init__(self, scene, x, y, group, anchor):
        super().__init__(scene, x, y)
        self.group, self.anchor = group, anchor

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def updateVisual(self):
        pass

    @abstractmethod
    def getScreenDimensions(self) -> (int, int):
        pass

    def getAnchorScreenOffsets(self) -> (int, int):
        w, h = self.getScreenDimensions()
        anchor = self.anchor

        return self._getAnchorScreenOffsets(anchor, w, h)

    @staticmethod
    def _getAnchorScreenOffsets(anchor, w, h) -> (int, int):
        x_offset, y_offset = 0, 0
        ax, ay = anchor[1], anchor[0]
        if ax == 'c':
            x_offset = -w // 2
        elif ax == 'r':
            x_offset = -(w - 1)

        if ay == 'c':
            y_offset = -h // 2
        elif ay == 't':
            y_offset = -(h - 1)

        return x_offset, y_offset

    def getAnchoredScreenPosition(self, anchor="bl") -> (int, int):
        x, y = self.getScreenPosition()

        ddx, ddy = self._getAnchorScreenOffsets(self.anchor, *self.getScreenDimensions())
        dx, dy = self._getAnchorScreenOffsets(anchor, *self.getScreenDimensions())

        return x + ddx - dx, y + ddy - dy

    def getAnchoredPosition(self, anchor="bl") -> (int, int):
        cx, cy = self.getAnchoredScreenPosition(anchor)
        return self.scene.game.camera.screenToGameCoords(cx, cy)

    def getDimensions(self):
        cw, ch = self.getScreenDimensions()
        return self.scene.game.camera.screenToGameCoords(cw, ch)

    @abstractmethod
    def setActive(self, active: bool):
        pass

    @abstractmethod
    def setColor(self, color):
        pass

    @abstractmethod
    def setScale(self, scale):
        pass

    @abstractmethod
    def setScreenPosition(self, cx, cy):
        pass

    def setAnchor(self, anchor):
        self.anchor = anchor
        self.updateVisual()

    def collision(self, obj: 'AbstractGameVisualObject') -> bool:
        x0, y0 = self.getAnchoredScreenPosition("bl")
        w0, h0 = self.getScreenDimensions()
        x1, y1 = obj.getAnchoredScreenPosition("bl")
        w1, h1 = obj.getScreenDimensions()

        xcheck = x0 <= x1 < x0 + w0 or x1 <= x0 < x1 + w1
        ycheck = y0 <= y1 < y0 + h0 or y1 <= y0 < y1 + h1

        return xcheck and ycheck

    def insideObject(self, cx: int, cy: int) -> bool:
        x0, y0 = self.getAnchoredScreenPosition("bl")
        w0, h0 = self.getScreenDimensions()
        return x0 <= cx < x0+w0 and y0 <= cy < y0+h0

    def distanceFromPoint(self, px, py):
        if self.insideObject(px, py):
            return 0
        x, y = self.getAnchoredPosition("bl")
        w, h = self.getDimensions()

        dx = min(abs(x-px), abs(x+w-px))
        dy = min(abs(y-py), abs(x+h-py))

        return (dx**2 + dy**2)**(1/2)


class AbstractSpriteGameObject(AbstractGameVisualObject):
    def __init__(self, scene, x, y, group, anchor, sprite):
        super().__init__(scene, x, y, group, anchor)

        self.sprite = sprite
        self.sprite.update(scale=SettingsGlobal.Scale)

    @abstractmethod
    def update(self, dt):
        pass

    def updateVisual(self):
        self.sprite.x, self.sprite.y = self.getAnchoredScreenPosition()

    def getScreenDimensions(self) -> (int, int):
        return self.sprite.width, self.sprite.height

    def getColor(self, ):
        return self.sprite.color

    def setActive(self, active: bool):
        self.sprite.visible = active

    def setScreenPosition(self, cx, cy):
        self.setPosition(*self.scene.game.camera.screenToGameCoords(cx, cy))

    def setColor(self, color):
        self.sprite.color = color

    def setScale(self, scale):
        self.sprite.scale = scale * SettingsGlobal.Scale

    def setOpacity(self, opacity):
        self.sprite.opacity = opacity

    def remove(self):
        if self.isRemoved():
            return
        self.sprite.delete()
        super().remove()


class SpriteGameObject(AbstractSpriteGameObject):
    def __init__(self, scene, x, y, group, anchor, asset):
        sprite = Sprite(asset.get(), batch=scene.batch, group=group)
        super().__init__(scene, x, y, group, anchor, sprite)

        self.asset = asset

    def update(self, dt):
        pass

    def updateImage(self, asset):
        self.asset = asset
        self.sprite.image = asset.get()


class TextGameObject(AbstractGameVisualObject):
    def __init__(self, scene, x, y, group, anchor, text, scale=1, multiline=False, width=1, bgcolor=None):
        super().__init__(scene, x, y, group, anchor)

        self.text = text
        self.scale = SettingsGlobal.Scale*scale
        fontSize = self.getFontSize()
        self.label = Label(text, font_name='Times New Roman', font_size=fontSize, x=x, y=y, batch=scene.batch, group=group,
                           anchor_x='left', anchor_y='bottom', multiline=multiline, width=width)

    def update(self, dt):
        pass

    def updateVisual(self):
        self.label.x, self.label.y = self.getAnchoredScreenPosition()

    def updateSize(self):
        self.label.font_size = self.getFontSize()

    def getScreenDimensions(self) -> (int, int):
        return self.label.content_width, self.label.content_height

    def getFontSize(self):
        return int(SettingsGlobal.FontSize*self.scale)

    def setText(self, text):
        self.text = text
        self.label.text = text

    def setActive(self, active: bool):
        self.label.visible = active

    def setScreenPosition(self, cx, cy):
        dx, dy = self.getAnchorScreenOffsets()
        self.label.x, self.label.y = cx + dx, cy + dy

    def setColor(self, color):
        if len(color) == 3:
            r, g, b = color
            color = (r, g, b, 255)
        self.label.color = color

    def setScale(self, scale):
        self.scale = scale*SettingsGlobal.Scale
        self.updateSize()

    def remove(self):
        if self.isRemoved():
            return
        self.label.delete()
        super().remove()


class BaseButton(AbstractGameObject):
    # states
    Default = 0
    Hovered = 1

    def __init__(self, gameVisualObject, f, args=None):
        super().__init__()
        self.gameVisualObject: AbstractGameVisualObject = gameVisualObject
        self.scene = gameVisualObject.scene

        self.f, self.args = f, args
        self.colorDefault, self.colorHovered = (127, 127, 127), (255, 255, 255)
        self.setColor(self.colorDefault)

        self.state = self.Default
        self.updateState(ignoreClick=True)

    def update(self, dt):
        self.updateState()

    def press(self):
        if self.args is None:
            self.f()
        else:
            self.f(*self.args)

    def updateState(self, ignoreClick=False):
        controller = self.scene.game.controller
        mousePosition = controller.mousePosition
        inside = self.gameVisualObject.insideObject(*mousePosition)

        if inside:
            self.setState(self.Hovered)
        else:
            self.setState(self.Default)

        if self.state == self.Hovered and controller.isControlPressed(controller.click) and not ignoreClick:
            self.press()

    def setState(self, state):
        if self.state == state:
            return
        self.state = state
        if state == self.Default:
            self.setColor(self.colorDefault)
        elif state == self.Hovered:
            self.setColor(self.colorHovered)

    def setColor(self, color):
        self.gameVisualObject.setColor(color)

    def setColors(self, colorDefault, colorHovered):
        self.colorDefault, self.colorHovered = colorDefault, colorHovered
        if self.state == self.Hovered:
            self.setColor(self.colorHovered)
        else:
            self.setColor(self.colorDefault)

    def setScale(self, scale):
        self.gameVisualObject.setScale(scale)

    def remove(self):
        super().remove()
        if not self.gameVisualObject.isRemoved():
            self.gameVisualObject.remove()


class HoverDisplay(AbstractGameObject):
    DisplayActive = False
    """Displays information when hovering over parent"""
    def __init__(self, parent, textSource=None, delay=0.2):
        super().__init__()
        self.parent: AbstractGameVisualObject = parent
        if textSource is None:
            textSource = parent
        self.textSource = textSource
        self.parent.addAssociate(self)
        self.label, self.labelBackground = None, None
        self.delay = delay
        self.hoverState, self.hoverTime, self.hoverPosition = 0, 0, (-1, -1)

    def update(self, dt):
        controller = self.parent.scene.game.controller
        mpos = controller.mousePosition

        inside = self.parent.insideObject(*mpos)

        clickHeld = controller.isControlHeldDown(controller.click)

        if self.hoverState == 2 and ((not inside and not self.label.insideObject(*mpos)) or clickHeld):
            HoverDisplay.DisplayActive = False
            self.hoverState, self.hoverTime, self.hoverPosition = 0, 0, (-1, -1)
            self.label.remove()
            self.labelBackground.remove()
            self.label = None

        if inside and not clickHeld and self.hoverState < 2:
            if self.hoverPosition != mpos:
                self.hoverTime = 0
                self.hoverPosition = mpos
            self.hoverTime += dt

            if self.hoverTime >= self.delay and not HoverDisplay.DisplayActive:
                self.hoverState = 2
                HoverDisplay.DisplayActive = True
                self.createLabel()

        if (not inside or clickHeld) and self.hoverState < 2:
            self.hoverState, self.hoverTime, self.hoverPosition = 0, 0, (-1, -1)

        if self.hoverState == 2:
            self.updateText()

    def createLabel(self):
        cx, cy = self.hoverPosition
        cx += 15
        x, y = self.parent.scene.game.camera.screenToGameCoords(cx, cy)
        x = int(x)
        y = int(y)

        text = self.getText()
        self.label = TextGameObject(self.parent.scene, x, y, TextGameObject.Group.TextDisplay, "cc", text, multiline=True, width=SettingsGlobal.hoverDisplayWidth*SettingsGlobal.Scale)
        w, h = self.label.getScreenDimensions()
        screen_w, screen_h = self.parent.scene.game.camera.screenWidth, self.parent.scene.game.camera.screenHeight

        if cy - h >= 0:
            anchor = "t"
        else:
            anchor = "b"
        if cx + w < screen_w:
            anchor += "l"
        else:
            anchor += "r"

        self.label.setAnchor(anchor)
        w, h = self.label.getDimensions()
        self.labelBackground = BoxObject(self.parent.scene, x, y, TextGameObject.Group.TextDisplayBackground, anchor, w, h, color=(31, 31, 31), opacity=191)

    def getText(self):
        getHoverText = getattr(self.textSource, "getHoverText", False)
        if callable(getHoverText):
            text = getHoverText()
        elif type(self.textSource) is str:
            text = self.textSource
        else:
            text = "default text"
        return text

    def updateText(self):
        self.label.setText(self.getText())

    def signalAssociateRemoval(self, obj):
        if obj is self.parent:
            self.remove()

    def remove(self):
        if self.label:
            self.label.remove()
            self.labelBackground.remove()
            HoverDisplay.DisplayActive = False
        super().remove()


class BoxObject(AbstractSpriteGameObject):

    def __init__(self, scene, x, y, group, anchor, w, h, screenDimensions=False, color=(0, 0, 0), opacity=255):
        w, h = self.convertDimensions(w, h, screenDimensions)
        img = self.createBox(w, h, scene.batch, group, color, opacity)
        super().__init__(scene, x, y, group, anchor, img)

    def update(self, dt):
        pass

    @staticmethod
    def convertDimensions(w, h, gameDimensions):
        if gameDimensions:
            scale = SettingsGlobal.Scale
        else:
            scale = 1
        w = w//scale + 1*(w % scale > 0)
        h = h//scale + 1*(h % scale > 0)
        return int(w), int(h)

    @staticmethod
    def createBox(w, h, batch, group, color=(0, 0, 0), opacity=255):
        r, g, b = color
        pixel = b''
        for i in [r, g, b, opacity]:
            pixel += i.to_bytes(1, 'big')
        data = pixel*w*h

        img = image.ImageData(w, h, "RGBA", data)

        texture = img.get_texture()
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        return Sprite(img, batch=batch, group=group)


class LineObject(AbstractGameVisualObject):

    def __init__(self, scene, x, y, x2, y2, group):
        anchor = ""
        if y < y2:
            anchor += "b"
        else:
            anchor += "t"
        if x < x2:
            anchor += "l"
        else:
            anchor += "r"

        super().__init__(scene, x, y, group, anchor=anchor)
        self.x2, self.y2 = x2, y2

        camera = self.scene.game.camera
        x, y = camera.gameToScreenCoords(x, y)
        x2, y2 = camera.gameToScreenCoords(x2, y2)
        self.shape = Line(x, y, x2, y2, width=SettingsGlobal.Scale/2, batch=scene.batch, group=group)

    def update(self, dt):
        pass

    def updateVisual(self):
        self.shape.x, self.shape.y = self.getAnchoredScreenPosition(self.anchor)

    def getScreenDimensions(self) -> (int, int):
        return abs(self.shape.x - self.shape.x2), abs(self.shape.y - self.shape.y2)

    def setActive(self, active: bool):
        self.shape.visible = active

    def setColor(self, color):
        if len(color) == 3:
            r, g, b = color
            color = (r, g, b, 255)
        self.shape.color = color

    def setScale(self, scale):
        pass

    def setScreenPosition(self, cx, cy):
        self.shape.x, self.shape.y = cx, cy

    def remove(self):
        super().remove()
        self.shape.delete()
