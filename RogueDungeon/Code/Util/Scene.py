from abc import ABC, abstractmethod
from pyglet import graphics

import Code.Game
from Code.Util.GameObject import AbstractGameObject


class Scene(ABC):
    def __init__(self, game):
        self.game: Code.Game.Game = game
        self.switchState = None

        # render stuff
        self.batch = graphics.Batch()
        self.window = game.window

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def handleInput(self, dt):
        pass

    def draw(self):
        self.window.clear()
        self.batch.draw()
        self.window.flip()

    def clear(self):
        AbstractGameObject.clear()

    def setSwitchState(self, state):
        self.switchState = state
