import time

from pyglet import clock
from pyglet.window import Window

from Code.Encounters.EncounterMap import EncounterMap
from Code.Entities.PlayerData import PlayerData
from Code.Logic.Inventory import Inventory
from Code.Scenes.DeckScene import DeckScene
from Code.Scenes.MapScene import MapScene
from Code.Util.Saves import *

from Code.Scenes.BattleScene import BattleScene
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.SystemStuff import SystemStuff
from Code.Util.Camera import Camera
from Code.Util.Controller import Controller
from Code.Util.GameObject import AbstractGameObject
from Code.Scenes.MainScene import MainScene


class Game:
    def __init__(self):
        self.dt, self.time, self.tick = 0, 0, 0
        self.run = False

        self.showFps = SettingsGlobal.ShowFPS
        self.time0 = 0
        self.timeFrameStart = 0.0

        # Camera/window stuff
        x, y = 0, 0
        res_w, res_h = SettingsGlobal.Width, SettingsGlobal.Height
        w, h = SystemStuff.getDefaultScreenResolution()

        if SettingsGlobal.Fullscreen:
            SettingsGlobal.Scale = min(w // res_w,  h // res_h)
        else:
            SettingsGlobal.Scale = min(6*w//(res_w*8), 6*h//(res_h*8))
        width, height = res_w*SettingsGlobal.Scale, res_h*SettingsGlobal.Scale
        self.camera: Camera = Camera(x, y, width, height, SettingsGlobal.Scale)

        caption = SettingsGlobal.GameName

        if SettingsGlobal.Fullscreen:
            self.window = Window(fullscreen=SettingsGlobal.Fullscreen, caption=caption)
        else:
            self.window = Window(width=width, height=height, caption=caption)

        # Setup controller
        self.controller = Controller(self.window)

        # Game Data
        self.loadData()

        # Scene
        self.scene = MainScene(self)

    def start(self):
        self.run = True
        while self.run:
            self.dt = clock.tick()
            self.loop()

        self.end()

    def loop(self):
        self.updateFpsInfo()

        self.handleInput()
        if self.controller.isControlPressed(Controller.pause):
            return

        self.scene.update(self.dt)
        self.handleScene()
        AbstractGameObject.updateActiveObjects(self.dt)
        self.scene.draw()

        self.controller.updateReset()

    def updateFpsInfo(self):
        self.time += self.dt
        self.tick += 1

        # print("frame", self.tick, 1/self.dt, "FPS")

        if self.showFps and self.tick%10 == 0:
            dt = self.time - self.time0
            self.time0 = self.time
            if dt*6 > 1.1:
                x = "SLOW!!"
            else:
                x = ""
            print(dt*6, "FPS", x)

    def handleInput(self):
        self.dispatchEvents()
        self.controller.update(self.dt)

        if self.controller.isControlPressed(Controller.close):
            self.run = False
            return

        if self.controller.isControlPressed(Controller.pause):
            self.controller.updateReset()
            return

    def handleScene(self):
        if not self.scene.switchState:
            return

        if self.scene.switchState == "MAP":
            save(self.inventory, "inventory")
            self.setScene(MapScene)
        elif self.scene.switchState == "MAIN":
            self.setScene(MainScene)
        elif self.scene.switchState == "DECK":
            self.setScene(DeckScene)
        elif self.scene.switchState == "BATTLE":
            self.setScene(BattleScene)

    def setScene(self, sceneClass):
        if self.scene is not None:
            self.scene.clear()
        self.scene = sceneClass(self)

    def end(self):
        pass

    def close(self):
        self.window.close()

    def dispatchEvents(self):
        return self.window.dispatch_events()

    def clear(self):
        self.window.clear()

    def flip(self):
        self.window.flip()

    def onNewGame(self):
        self.inventory = loadSave("", Inventory)
        self.encounterMap = loadSave("", EncounterMap)
        self.playerData = loadSave("", PlayerData)

    def saveData(self):
        save(self.inventory, "inventory")
        save(self.encounterMap, "encounterMap")
        save(self.playerData, "playerData")

    def loadData(self):
        self.inventory = loadSave("inventory", Inventory)
        self.encounterMap = loadSave("encounterMap", EncounterMap)
        # self.encounterMap.show()
        self.playerData = loadSave("playerData", PlayerData)

    def resetSave(self):
        pass

    def tickClock(self):
        """Alternative clock ticker"""
        if self.timeFrameStart == 0.0:
            self.dt = 1/60
            self.timeFrameStart = time.perf_counter()
            return

        target = self.timeFrameStart + 1/60
        while time.perf_counter() < target and False:
            _ = 5
            _ += 5
        curTime = time.perf_counter()

        self.dt = curTime - self.timeFrameStart
        # print(1/self.dt)
        self.timeFrameStart = curTime
