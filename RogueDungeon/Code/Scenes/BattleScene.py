import random

from Code.Logic.Button import ButtonText, ButtonSprite
from Code.Entities.Enemies import *
from Code.Entities.Player import Player
from Code.Util.Assets import Img
from Code.Util.GameObject import SpriteGameObject
from Code.Util.StateHandler import StateHandler

from Code.Util.Scene import Scene
from Code.Util.SettingsGlobal import SettingsGlobal


class BattleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.setConstants()

        self.createBackground()
        self.createButtons()

        self.stateHandler = StateHandler(self, "start")

        # convert to list with duplicate runes instead of counts
        self.deck = self.game.inventory.getDeckDuplicates()

        self.player = Player(self, *self.getPlayerEntityPosition())
        self.enemies = []
        for enemy in self.game.encounterMap.currentEncounter.encounter.battle.enemies:
            self.addEnemy(enemy(self, 0, 0))

        self.hand = []

        self.selectedRuneInfo = None

    def update(self, dt):
        self.handleInput(dt)
        if not self.player.isAlive:
            if not self.stateHandler.isActive(self, "player died"):
                self.stateHandler.interrupt(self, "player died")
                self.onPlayerDied()
        self.stateHandler.update(dt)

    def updateState(self, dt, state):
        if state == "start":
            self.onEnterPlayerTurn()
            self.stateHandler.setState(self, "player")
        elif state == "player":
            if self.hasWon():
                self.stateHandler.setState(self, "won")
                self.onWin()
                self.stateHandler.update(dt)
                return
            self.handleInputPlayerTurn(dt)
        elif state == "enemy":
            self.onEnemyTurn()
        elif state == "won":
            pass
        elif state == "player died":
            pass

    def handleInput(self, dt):
        pass

    def handleInputPlayerTurn(self, dt):
        controller = self.game.controller
        cx, cy = controller.mousePosition

        if self.selectedRuneInfo is None and controller.isControlPressed(controller.click):
            for cardObject in self.hand:
                if cardObject.insideObject(cx, cy):
                    self.selectRune(cardObject)
                    break

        self.handleInputSelectedCard(dt, controller)

    def handleInputSelectedCard(self, dt, controller):
        if self.selectedRuneInfo is None:
            return

        if not controller.isControlHeldDown(controller.click):
            self.checkRuneUse(controller)
            self.orderHand()
            self.unselectCard()
            return

        dx, dy = self.game.camera.screenToGameCoords(*controller.mouseMotion)
        cardObject, pos = self.selectedRuneInfo
        x, y = cardObject.getPosition()
        cardObject.setPosition(x + dx, y + dy)

    def getEnemyBattlePosition(self, enemy):
        position = 0
        for e in self.enemies:
            if e is enemy:
                return position
            position += e.size

        print("Enemy not on field")
        return -1

    def getEnemyPosition(self, enemy):
        return self.enemies.index(enemy)

    def getEnemiesLength(self):
        """
        :return: length of enemies list while taking enemy size into account
        """
        return sum([enemy.size for enemy in self.enemies])

    def getPlayerEntityPosition(self):
        return self.playerPosition0

    def getEnemyEntityPosition(self, position=0, width=1):
        x, y = self.enemyPosition0
        x += position*self.enemyOffsetX + (width-1)*self.enemyOffsetX//2
        return x, y

    def getCardEntityPosition(self, position=0):
        x, y = self.runePosition0
        x += position*self.runeOffsetX
        return x, y

    def setConstants(self):
        self.runePosition0 = (24, 135)
        self.runeOffsetX = 23

        self.playerPosition0 = (40, 29)
        self.enemyPosition0 = (140, 29)
        self.enemyOffsetX = 48

        self.endTurnButtonPosition = (290, 179)

    def setEnemyPosition(self, enemy, position, instantly=True):
        x, y = self.getEnemyEntityPosition(position, enemy.size)
        if instantly:
            enemy.setPosition(*self.getEnemyEntityPosition(position, enemy.size))
        else:
            enemy.moveTo(x, y)

    def addEnemy(self, enemy):
        position = self.getEnemiesLength()
        x, y = self.getEnemyEntityPosition(position, enemy.size)
        enemy.setPosition(x, y)

        self.enemies.append(enemy)

    def onEnterPlayerTurn(self):
        self.fillHand()
        for enemy in self.enemies:
            enemy.chooseAttack()
        self.player.onEnterTurn()

    def onEnemyTurn(self):
        if len(self.enemiesTurn):
            self.enemiesTurn.pop().onTurn(self.stateHandler)
        else:
            self.onEndEnemyTurn()
        return

    def onEndEnemyTurn(self):
        self.onEnterPlayerTurn()
        self.stateHandler.setState(self, "player")

    def onWin(self):
        self.game.encounterMap.currentEncounter.complete()
        x, y = self.game.camera.getCenter()
        self.winButton = ButtonText(self, x, y, "cc", "continue", self.setSwitchState, ("MAP",))
        self.winButton.setScale(3)
        self.game.encounterMap.currentEncounter.encounter.completeBattle()

        self.game.saveData()

    def onPlayerDied(self):
        self.game.encounterMap.currentEncounter.complete()
        x, y = self.game.camera.getCenter()
        self.playerDiedButton = ButtonText(self, x, y, "cc", "Main Screen", self.setSwitchState, ("MAIN",))
        self.playerDiedButton.setScale(3)
        self.game.resetSave()

    def isValidRuneUse(self, runeObject, enemy):
        valid = False
        for i in range(enemy.size):
            if runeObject.isValidUse(self.getEnemyBattlePosition(enemy) + i, enemy):
                valid = True
        return valid

    def createBackground(self):
        self.background = SpriteGameObject(self, 0, 0, SpriteGameObject.Group.Background, "bl", Img.Dungeon)

    def createButtons(self):
        x, y = self.endTurnButtonPosition
        self.winButton = None
        self.playerDiedButton = None
        self.turnButton = ButtonSprite(self, x, y, "tc", Img.EndTurn, self.endTurn)

    def checkRuneUse(self, controller):
        runeObject, pos = self.selectedRuneInfo

        # Is card used on anything?
        targets = []
        for enemy in self.enemies:
            position = self.getEnemyBattlePosition(enemy)
            if runeObject.collision(enemy) and self.isValidRuneUse(runeObject, enemy):
                targets.append(enemy)
        # If multiple, pick closest
        if len(targets) > 0:
            x, y = runeObject.getAnchoredPosition("cc")
            target = targets[0]
            distance = target.distanceFromPoint(x, y)
            for t in targets:
                d = t.distanceFromPoint(x, y)
                if d < distance:
                    distance = d
                    target = t

            runeObject.use(target)
            self.removeFromHand(runeObject)

    def selectRune(self, runeObject):
        self.selectedRuneInfo = runeObject, runeObject.getPosition()
        for enemy in self.enemies:
            if not self.isValidRuneUse(runeObject, enemy):
                enemy.setColor((63, 63, 63))

    def unselectCard(self):
        self.selectedRuneInfo = None
        for enemy in self.enemies:
            enemy.setColor((255, 255, 255))

    def drawFromDeck(self, n):
        drawnRunes = []
        for _ in range(n):
            if len(self.deck) == 0:
                break
            i = random.randint(0, len(self.deck)-1)
            rune = self.deck.pop(i)
            drawnRunes.append(rune)
        return drawnRunes

    def fillHand(self):
        nRunes = self.player.getRunesPerTurn()
        self.hand = [
            rune(self, *self.getCardEntityPosition(i)) for i, rune in enumerate(self.drawFromDeck(nRunes))
        ]
        self.orderHand()

    def clearHand(self, n=0):
        for rune in self.hand[n:]:
            rune.remove()
            self.deck.append(rune.getRune())
        self.hand = self.hand[:n]
        self.orderHand()

    def removeFromHand(self, runeObject):
        i = self.hand.index(runeObject)
        self.hand.pop(i)
        runeObject.remove()
        self.deck.append(runeObject.getRune())
        self.orderHand()

    def orderHand(self):
        for i, rune in enumerate(self.hand):
            rune.setPosition(*self.getCardEntityPosition(i))

    def orderEnemies(self, instantly=False):
        for enemy in self.enemies:
            position = self.getEnemyBattlePosition(enemy)
            self.setEnemyPosition(enemy, position, instantly)

    def endTurn(self):
        self.clearHand()
        if self.stateHandler.isActive(self, "player"):
            self.enemiesTurn = [e for e in self.enemies[::-1]]

            self.stateHandler.setState(self, "enemy")

    def moveEnemy(self, enemy, movement):
        if movement == 0:
            return

        # permutate list
        positionOld = self.getEnemyPosition(enemy)
        if movement > 0:
            positionNew = min(positionOld+movement, len(self.enemies)-1)

            enemiesNew = self.enemies[:positionOld]
            enemiesNew += self.enemies[positionOld+1:positionNew+1]
            enemiesNew += [enemy]
            enemiesNew += self.enemies[positionNew+1:]
            pass
        else:
            positionNew = max(positionOld + movement, 0)

            enemiesNew = self.enemies[:positionNew]
            enemiesNew += [enemy]
            enemiesNew += self.enemies[positionNew:positionOld]
            enemiesNew += self.enemies[positionOld+1:]
            pass

        self.enemies = enemiesNew
        self.orderEnemies()

    def replaceEnemy(self, enemy, corpse):
        if enemy not in self.enemies:
            print("replaceEnemy from levelScene", "Enemy not in list")
            return

        position = self.getEnemyPosition(enemy)

        if corpse is None:
            self.enemies.pop(position)
        else:
            self.enemies[position] = corpse
        self.orderEnemies()

    def hasWon(self):
        for enemy in self.enemies:
            if not enemy.stats.isCorpse:
                return False
        return True
