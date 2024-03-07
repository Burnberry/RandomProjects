import random
from random import choice

from Code.Entities.Entity import Entity
from Code.Stats.EnemyAttackStats import EnemyAttackStatsBase
from Code.Stats.EntityStats import *
from Code.Util.Assets import Img
from Code.Util.GameObject import TextGameObject, HoverDisplay


class Enemy(Entity):
    def __init__(self, scene, x, y, data, asset=Img.Box):
        self.stats = data
        super().__init__(scene, x, y, entityData=data, asset=asset)
        self.attack: EnemyAttackStatsBase
        self.attackDisplay = None
        self.turns = -1
        HoverDisplay(self)

    def updateState(self, dt, state):
        if state == "preAttack":
            self.delay -= dt
            if self.delay <= 0:
                self.delay = 0.8
                text = self.attack.getAttackStats(self.getBattlePosition()).name
                self.createFloatingTextEffect(text, ttl=self.delay, speed=12, scale=2)
                self.stateHandler.setState(self, "attack")
        elif state == "attack":
            self.delay -= dt
            if self.delay <= 0:
                self.onAttack()
                self.delay = 0.5
                self.setColor((255, 255, 255))
                self.stateHandler.setState(self, "buffer")
        elif state == "buffer":
            self.delay -= dt
            if self.delay <= 0:
                self.stateHandler.release()
        else:
            self.stateHandler.release()

    def getName(self):
        return self.stats.name

    def getHoverText(self):
        text = self.stats.name + "\n"
        if len(self.stats.description):
            text += self.stats.description + "\n"

        return text[:-1]

    def getBattlePosition(self):
        return self.scene.getEnemyBattlePosition(self)

    def getAttack(self, attackClass):
        for attack in self.stats.attacks:
            if type(attack) == attackClass:
                return attack

        print("No attack found with name:", attackClass)

    def setAttackDisplay(self):
        if not self.isAlive:
            return
        if self.attackDisplay is not None:
            self.attackDisplay.remove()
        self.attackDisplay = self.createAttackDisplay()
        self.orderObjects()

    def setAttackText(self):
        if not self.isAlive:
            return
        text = self.attack.getDisplayText(self.turns)
        self.attackDisplay.setText(text)

    def setPosition(self, x, y):
        super().setPosition(x, y)
        self.orderObjects()

    def onDeath(self):
        super().onDeath()
        corpseType = self.stats.corpse
        if corpseType is None:
            corpse = None
        else:
            corpse = corpseType(self.scene, *self.getPosition())
        self.scene.replaceEnemy(self, corpse)
        self.corpse = corpse
        if self.attackDisplay is not None:
            self.attackDisplay.remove()
        self.remove()

    def onTurn(self, stateHandler):
        self.onEnterTurn()
        if self.stunned:
            self.createStunEffect()
            return
        if self.stats.isCorpse:
            return
        self.setAttackText()
        if not self.isAlive:
            return

        if self.attack.turns > self.turns:
            return
        self.turns = -1
        self.stateHandler = stateHandler
        self.stateHandler.interrupt(self, "preAttack")
        self.delay = 0
        self.setColor((180, 180, 180))

    def onEnterTurn(self):
        if not self.stunned:
            self.turns += 1
        super().onEnterTurn()

    def onAttack(self):
        if self.attack is None:
            self.attack = Stumble()
        position = self.getBattlePosition()
        attack = self.attack.getAttackStats(position)
        player = self.scene.player

        player.onAttacked(attack, self)

        if attack.buffs is not None:
            if attack.isAreaBuff:
                enemies = self.scene.enemies
            else:
                enemies = [self]
            for enemy in enemies:
                enemy.onBuffs(attack.buffs)

        if attack.movement != 0:
            self.moveBattlePosition(attack.movement)

    def chooseAttack(self):
        if self.stats.isCorpse:
            return
        if self.turns >= 0:
            return
        self.turns = 0
        self.attack = self.AIChooseAttack()
        self.setAttackDisplay()

    def AIChooseAttack(self):
        return choice(self.stats.attacks)

    def createAttackDisplay(self):
        if not self.isAlive:
            return
        text = self.attack.getDisplayText(self.turns)
        textObj = TextGameObject(self.scene, 0, 0, TextGameObject.Group.Text, "tc", text)
        HoverDisplay(textObj, self.attack)
        return textObj

    def orderObjects(self):
        super().orderObjects()
        self.orderAttackDisplays()

    def orderAttackDisplays(self):
        if self.attackDisplay is None:
            return

        if len(self.stacks):
            obj = None
            for key in self.stacks:
                _, obj, _ = self.stacks[key]
                break
            _, cy = obj.getAnchoredScreenPosition("bl")
        else:
            _, cy = self.healthTag.getAnchoredScreenPosition("bl")
        cx, _ = self.getAnchoredScreenPosition("bc")
        x, y = self.scene.game.camera.screenToGameCoords(cx, cy)

        self.attackDisplay.setPosition(x, y)


class Spider(Enemy):
    def __init__(self, scene, x, y):
        data = StatsSpiderBase()
        super().__init__(scene, x, y, data, asset=Img.Spider)

    def AIChooseAttack(self):
        if self.getBattlePosition() >= 2:
            return self.stats.attacks[0]
        else:
            return self.stats.attacks[1]


class Spitter(Enemy):
    def __init__(self, scene, x, y):
        data = StatsSpitterBase()
        super().__init__(scene, x, y, data, asset=Img.Spitter)


class BlobSmall(Enemy):
    def __init__(self, scene, x, y):
        data = StatsBlobSmallBase()
        super().__init__(scene, x, y, data, asset=Img.BlobSmall)


class Blob(Enemy):
    def __init__(self, scene, x, y):
        data = StatsBlobBase()
        super().__init__(scene, x, y, data, asset=Img.Blob)


class Snail(Enemy):
    def __init__(self, scene, x, y):
        data = StatsSnailBase()
        super().__init__(scene, x, y, data, asset=Img.Snail)

    def AIChooseAttack(self):
        position = self.getBattlePosition()
        if position == 0:
            return VenomousHarpoon()
        else:
            return OozleForth()


class Bat(Enemy):
    def __init__(self, scene, x, y):
        data = StatsBat()
        super().__init__(scene, x, y, data, asset=Img.Bat)

    def AIChooseAttack(self):
        position = self.getBattlePosition()
        if position >= 2:
            return Swoop()
        else:
            return VampiricBite()


class AlbinoBat(Enemy):
    def __init__(self, scene, x, y):
        data = StatsAlbinoBat()
        super().__init__(scene, x, y, data, asset=Img.AlbinoBat)

    def AIChooseAttack(self):
        position = self.getBattlePosition()
        if position >= 2:
            return Swoop()
        elif position == 1:
            if random.randint(0, 1) == 0:
                return Swoop()
            else:
                return VampiricBite()
        else:
            return BloodDrain()


class Shroomite(Enemy):
    def __init__(self, scene, x, y):
        data = StatsShroomite()
        super().__init__(scene, x, y, data, asset=Img.Shroomite)

    def AIChooseAttack(self):
        position = self.getBattlePosition()
        if position <= random.randint(0, 2):
            return Ram()
        else:
            return Wiggle()


class Toadstool(Enemy):
    def __init__(self, scene, x, y):
        data = StatsToadstool()
        super().__init__(scene, x, y, data, asset=Img.Toadstool)

        self.wiggles = 0

    def AIChooseAttack(self):
        if self.wiggles >= random.randint(3, 9):
            self.wiggles -= 1
            return Sporulate()
        else:
            self.wiggles += random.randint(1, 3)
            return Wiggle()


class Mudslinger(Enemy):
    def __init__(self, scene, x, y):
        data = StatsMudslinger()
        super().__init__(scene, x, y, data, asset=Img.Mudslinger)

    def AIChooseAttack(self):
        position = self.getBattlePosition()
        if position >= 2 and random.randint(0, 3) > 0:
            return MudSling()

        if self.getStackCount("block") == 0 and random.randint(0, 2) > 0:
            return Harden()

        return MudCoats()


class RotBlobSmall(Enemy):
    def __init__(self, scene, x, y):
        data = StatsRotBlobSmall()
        super().__init__(scene, x, y, data, asset=Img.RotBlobSmall)

    def AIChooseAttack(self):
        return Slam()


class HobBlobSmall(Enemy):
    def __init__(self, scene, x, y):
        data = StatsHobBlobSmall()
        super().__init__(scene, x, y, data, asset=Img.HobBlobSmall)

    def AIChooseAttack(self):
        return Slam()


class Sprigat(Enemy):
    def __init__(self, scene, x, y):
        data = StatsSprigat()
        super().__init__(scene, x, y, data, asset=Img.Sprigat)

    def AIChooseAttack(self):
        position = self.getBattlePosition()
        if position == 0:
            return FoulFlower()
        return Shriek()


# Corpses
class CorpseSmall(Enemy):
    def __init__(self, scene, x, y):
        data = StatsCorpseSmallBase()
        super().__init__(scene, x, y, data, asset=Img.CorpseSmall)


class Corpse(Enemy):
    def __init__(self, scene, x, y):
        data = StatsCorpseBase()
        super().__init__(scene, x, y, data, asset=Img.Corpse)
