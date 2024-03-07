from pyglet import clock

from win32api import GetSystemMetrics

from Code.Util.Camera import Camera
from Code.Util.Controller import Controller
from Code.Util.GameObject import GameObject
from Code.Util.SoundPlayer import SoundPlayer
from Code.Util.Settings import Settings
from Code.Logic.LineGenerator import LineGenerator
from Code.Logic.Level import Level


class Game:
    def __init__(self):
        self.tick = 0
        self.run = False
        self.dt = 0
        self.time = 0

        x, y = 0, 0
        screen_width, screen_height, offset = GetSystemMetrics(0)//2, GetSystemMetrics(1)//2, 24*Settings.Scale
        self.camera = Camera(x, y, screen_width, screen_height, offset, Settings.Fullscreen)

        # Setup controller
        self.controller = Controller(self.camera.window)

        # Drawing stuff
        self.batch = GameObject.batch

        # level
        self.level = None

        # player state
        self.player = None

        # Sound stuff
        self.soundPlayer = SoundPlayer(self.camera)

        self.lineGenerator = LineGenerator()

    def start(self):
        self.level: Level = Level(self)

        self.level.start()
        self.run = True
        while self.run:
            # Wait for frame and handle inputs
            self.dt = clock.tick()
            self.camera.dispatch_events()
            self.handle_input()

            if self.controller.is_control_pressed(Controller.pause):
                continue

            self.time += self.dt
            self.level.update(self.dt)
            GameObject.update_entities(self.dt)
            self.draw()

            self.tick += 1

            if self.dt > 1/50:
                print(self.tick, self.dt)

        self.end()

    def end(self):
        self.camera.close()

    def handle_input(self):
        if self.controller.is_control_held_down(Controller.close):
            self.run = False

        if self.controller.is_control_held_down(Controller.pause):
            self.controller.update()
            return

        self.level.handle_input()

        self.controller.update()

    def draw(self):
        self.camera.clear()
        self.batch.draw()
        self.camera.flip()

    ###############
    # Game specific stuff
    ###############
