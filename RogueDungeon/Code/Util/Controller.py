from pyglet.window import key as PygKey
from pyglet.window import mouse as PygMouse


class Controller:
    # general controls
    pause = "pause"
    close = "close"

    click = "click"

    # game controls
    up, down, left, right = "up", "down", "left", "right"

    def __init__(self, window):
        self.window = window

        self.mousePosition, self.mouseMotion = (0, 0), (0, 0)
        self.text = ""  # text written by player during frame

        self.controlToKeySet = dict()    # Keybind states
        self.keyToControl = dict()    # n key to 1 control mapping

        # define inputs (should be read from a file)
        self.controlToKeySet[Controller.up] = {PygKey.UP}
        self.controlToKeySet[Controller.down] = {PygKey.DOWN}
        self.controlToKeySet[Controller.left] = {PygKey.LEFT}
        self.controlToKeySet[Controller.right] = {PygKey.RIGHT}
        self.controlToKeySet[Controller.click] = {PygMouse.LEFT}

        # fill key_to_control
        for ctrl in self.controlToKeySet:
            for key in self.controlToKeySet[ctrl]:
                self.keyToControl[key] = ctrl

        # controls states (tracks numbers of keys pressing control)
        self.controlHeldDown = dict()
        self.controlPressed = dict()
        # fill
        for ctrl in self.controlToKeySet:
            self.controlHeldDown[ctrl] = 0
            self.controlPressed[ctrl] = 0

        self._pygletEventMapper()

    def _pygletEventMapper(self):
        @self.window.event
        def on_key_press(symbol, modifiers=None):
            control = self.getControl(symbol)
            if control:  # False if unused key
                self.pressControl(control)

        @self.window.event
        def on_key_release(symbol, modifiers=None):
            control = self.getControl(symbol)
            if control:  # False if unused key
                self.releaseControl(control)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            on_key_press(button, modifiers)
            self.resetControl(self.pause)

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            on_key_release(button, modifiers)

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.mousePosition = (x, y)
            mx, my = self.mouseMotion
            self.mouseMotion = (mx + dx, my + dy)

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.mousePosition = (x, y)
            mx, my = self.mouseMotion
            self.mouseMotion = (mx + dx, my + dy)

        @self.window.event
        def on_text(text):
            self.text += text

        @self.window.event
        def on_activate():
            self.resetControl(self.pause)

        @self.window.event
        def on_deactivate():
            # reset control state because inputs are no longer tracked until activated again
            self.reset()
            self.pressControl(self.pause)

        @self.window.event
        def on_close():
            self.pressControl(self.close)

        @self.window.event
        def on_move(x, y):
            self.reset()
            self.pressControl(self.pause)

        # Other possible actions: on_mouse_[action]
        # enter, leave, scroll, drag

    def getControl(self, key):
        return self.keyToControl.get(key, False)

    def getText(self):
        return self.text

    def getKeySet(self, control):
        return self.controlToKeySet.get(control, False)

    def update(self, dt):
        pass

    def updateReset(self):
        self.text = ""
        for control in self.controlPressed:
            self.controlPressed[control] = 0
        self.mouseMotion = (0, 0)

    def reset(self):
        self.updateReset()
        for control in self.controlHeldDown:
            self.resetControl(control)

    def pressControl(self, control):
        self.controlHeldDown[control] = self.controlHeldDown.get(control, 0) + 1
        self.controlPressed[control] = 1

    def releaseControl(self, control):
        self.controlHeldDown[control] = max(0, self.controlHeldDown.get(control, 0) - 1)

    def resetControl(self, control):
        self.controlHeldDown[control] = 0
        self.controlPressed[control] = 0

    def isControlPressed(self, control):
        return self.controlPressed.get(control, 0) > 0

    def isControlHeldDown(self, control):
        return self.controlHeldDown.get(control, 0) > 0
