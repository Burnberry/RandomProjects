from Code.Logic.Button import ButtonText
from Code.Util.Assets import Img
from Code.Util.GameObject import SpriteGameObject

from Code.Util.Scene import Scene
from Code.Util.SettingsGlobal import SettingsGlobal


class MainScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.createBackground()
        self.createButtons()

    def update(self, dt):
        self.handleInput(dt)

    def handleInput(self, dt):
        controller = self.game.controller
        x, y = controller.mousePosition

    def createBackground(self):
        self.background = SpriteGameObject(self, 0, 0, SpriteGameObject.Group.Background, "bl", Img.Dungeon)
        self.background.setColor((127, 127, 127))

    def createButtons(self):
        x, y = self.game.camera.getCenter()
        self.startButton = ButtonText(self, x, y + 12, 'cc', "START", self.setSwitchState, ("MAP",))
        self.newGameButton = ButtonText(self, x, y - 12, 'cc', "NEW GAME", self.onNewGame)

        self.startButton.setScale(3)
        self.newGameButton.setScale(3)

    def onNewGame(self):
        self.game.onNewGame()
        self.setSwitchState("MAP")
