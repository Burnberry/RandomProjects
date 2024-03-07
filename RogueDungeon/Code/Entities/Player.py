from Code.Entities.Entity import Entity
from Code.Stats.EntityStats import StatsPlayerBase
from Code.Util.Assets import Img
from Code.Util.GameObject import HoverDisplay


class Player(Entity):
    def __init__(self, scene, x, y):
        data = StatsPlayerBase()
        self.stats = data
        super().__init__(scene, x, y, entityData=data, asset=Img.Player)

        self.playerData = self.scene.game.playerData
        self.setHealth(self.playerData.getHealth())
        HoverDisplay(self)

    def getHoverText(self):
        text = self.stats.name + "\n"
        if len(self.stats.description):
            text += self.stats.description + "\n"

        return text[:-1]

    def getName(self):
        return "Player"

    def getRunesPerTurn(self):
        stun = self.getStackCount("stun")
        if stun <= 0:
            return 4
        elif stun < 2:
            return 3
        else:
            return 2

    def setHealth(self, health):
        super().setHealth(health)
        self.playerData.health = self.health
