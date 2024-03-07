from Code.Logic.Button import ButtonText, ButtonSprite
from Code.Util.Assets import Img
from Code.Util.GameObject import SpriteGameObject
from Code.Util.Scene import Scene
from Code.Util.SettingsGlobal import SettingsGlobal


class DeckScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.setConstants()

        self.createBackground()
        self.createButtons()

        self.inventory = game.inventory
        self.shownDeck, self.shownRunes = [], []
        self.deckPage, self.runesPage = 0, 0

        self.createDeckEditor()

    def update(self, dt):
        self.handleInput(dt)

    def handleInput(self, dt):
        controller = self.game.controller
        x, y = controller.mousePosition

        if controller.isControlPressed(controller.click):
            for cardObject in self.shownDeck:
                if cardObject.insideObject(x, y):
                    self.inventory.removeFromDeck(type(cardObject))
                    self.createDeckEditor()
                    break

            for cardObject in self.shownRunes:
                if cardObject.insideObject(x, y):
                    self.inventory.addToDeck(type(cardObject))
                    self.createDeckEditor()
                    break

    def setConstants(self):
        self.colSize = 8

        self.dx = 24
        self.dy = 24
        self.xDeckPage, self.yDeckPage = 40, 140
        self.xRunePage, self.yRunePage = 40, 90

    def addDeckPage(self, n=1):
        self.deckPage += n
        self.createDeckEditor()

    def addRunesPage(self, n=1):
        self.runesPage += n
        self.createDeckEditor()

    def createDeckEditor(self):
        self.clearDeckEditor()

        self.createDeckPage()
        self.createRunePage()

    def createDeckPage(self):
        if len(self.inventory.deck) <= self.deckPage * self.colSize:
            self.deckPage = max(0, self.deckPage-1)

        x, y = self.xDeckPage, self.yDeckPage

        if self.deckPage > 0:
            self.deckLeftButton = ButtonSprite(self, x-10, y, 'br', self.addDeckPage, (-1,), Img.ArrowLeft)
        i = -1
        for rune, n in self.inventory.deck:
            i += 1
            if i < self.deckPage*self.colSize or i >= (self.deckPage+1)*self.colSize:
                continue
            cardObject = rune(self, x, y)
            cardObject.setText(str(n))
            self.shownDeck.append(cardObject)

            x += self.dx
        if len(self.inventory.deck) > (self.deckPage+1)*self.colSize:
            self.deckRightButton = ButtonSprite(self, x + 10, y, 'br', self.addDeckPage, (1,), Img.ArrowRight)

    def createRunePage(self):
        x, y = self.xRunePage, self.yRunePage

        if self.runesPage > 0:
            self.runesLeftButton = ButtonSprite(self, x - 10, y, 'br', self.addRunesPage, (-1,), Img.ArrowLeft)
        for i, rune in enumerate(self.inventory.runes):
            if i < self.runesPage * self.colSize or i >= (self.runesPage + 1) * self.colSize:
                continue
            n = self.inventory.runes[rune]
            k = n - self.inventory.deckCount(rune)
            cardObject = rune(self, x, y)
            cardObject.setText(str(k) + "/" + str(n))
            if k <= 0:
                r, g, b = cardObject.getColor()
                cardObject.setColor((r // 2, g // 2, b // 2))
            self.shownRunes.append(cardObject)

            x += self.dx
        if len(self.inventory.runes) > (self.runesPage + 1) * self.colSize:
            self.runesRightButton = ButtonSprite(self, x + 10, y, 'br', self.addRunesPage, (1,), Img.ArrowRight)

    def createBackground(self):
        self.background = SpriteGameObject(self, 0, 0, SpriteGameObject.Group.Background, "bl", Img.Dungeon)
        self.background.setColor((127, 127, 127))

    def createButtons(self):
        self.deckLeftButton, self.deckRightButton, self.runesLeftButton, self.runesRightButton = None, None, None, None
        x, y = self.game.camera.getCenter()
        self.backButton = ButtonText(self, 280, 160+8, 'cc', "BACK", self.setSwitchState, ("MAP",))

        self.backButton.setScale(3)

    def clearDeckEditor(self):
        for obj in self.shownDeck + self.shownRunes:
            obj.remove()
        self.shownDeck, self.shownRunes = [], []
        for obj in [self.deckLeftButton, self.deckRightButton, self.runesLeftButton, self.runesRightButton]:
            if obj is not None:
                obj.remove()
        self.deckLeftButton, self.deckRightButton, self.runesLeftButton, self.runesRightButton = None, None, None, None
