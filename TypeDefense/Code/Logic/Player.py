from pyglet import media

from Code.Logic.Entity import Entity
from Code.Util.Controller import Controller
from Code.Util import Assets


class Player(Entity):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        #self.set_visible(False)

    def update(self, dt):
        self.controller.reset()
        super().update(dt)
