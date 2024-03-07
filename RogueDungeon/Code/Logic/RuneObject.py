from abc import abstractmethod

from Code.Util.Assets import Img
from Code.Util.GameObject import SpriteGameObject, TextGameObject, HoverDisplay
from Code.Stats.RuneStats import *


class RuneObject(SpriteGameObject):
    def __init__(self, scene, x, y, group=SpriteGameObject.Group.Foreground, anchor='bc', asset=Img.Box, stats=RuneStatsBaseBasicAttack()):
        super().__init__(scene, x, y, group, anchor, asset)
        self.stats = stats
        self.label = None
        self.hoverDisplay = HoverDisplay(self)

    def use(self, target):
        if self.stats.isAreaAttack:
            for target in self.scene.enemies.copy():
                target.onAttacked(self.stats, self.scene.player)
        else:
            target.onAttacked(self.stats, self.scene.player)

    def getRune(self):
        return type(self)

    def update(self, dt):
        pass

    def remove(self):
        super().remove()
        if self.label:
            self.label.remove()

    def setPosition(self, x, y):
        super().setPosition(x, y)
        if self.label is not None:
            self.label.setPosition(x, y)

    def setText(self, text):
        if self.label is None:
            x, y = self.getPosition()
            self.label = TextGameObject(self.scene, x, y, SpriteGameObject.Group.Text, "tc", text)
        else:
            self.label.text = text

    def isValidUse(self, position, enemy):
        return self.stats.isValidUse(position, enemy)

    def getHoverText(self):
        return self.stats.getHoverText()
