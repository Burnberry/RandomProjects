from pyglet.window import key as Key
from pyglet.window import mouse as Mouse

from Code.Util.Iter import Iter


class Controller:

    # Define game controls
    close = Iter.i()
    pause = Iter.i()
    submit = Iter.i()  # Control to submit typed text
    backspace = Iter.i()
    up, down, left, right = Iter.i(), Iter.i(), Iter.i(), Iter.i()

    def __init__(self, window):
        # Text written by player during frame
        self.text = ""

        # Window is source of player inputs
        self.window = window

        # Keybind states
        self.control_to_key_set = dict()
        # Note that below could be a set instead if a key could be used for different controls (combat vs UI navigation)
        self.key_to_control = dict()
        self.key_to_text = dict()

        # Define inputs
        # Note: should ideally be read from a settings file
        self.control_to_key_set[Controller.submit] = {Key.ENTER}
        self.control_to_key_set[Controller.backspace] = {Key.BACKSPACE}
        self.control_to_key_set[Controller.up] = {Key.UP}
        self.control_to_key_set[Controller.down] = {Key.DOWN}
        self.control_to_key_set[Controller.left] = {Key.LEFT}
        self.control_to_key_set[Controller.right] = {Key.RIGHT}

        # fill key_to_control
        for control in self.control_to_key_set:
            for key in self.control_to_key_set[control]:
                self.key_to_control[key] = control

        # controls state
        self.control_held_down = dict()
        self.control_pressed = dict()
        # fill
        for control in self.control_to_key_set:
            self.control_held_down[control] = 0
            self.control_pressed[control] = 0
        self.mouse_position = (0, 0)

        # Bind input source to controller
        @self.window.event
        def on_key_press(symbol, modifiers=None):
            control = self.get_control(symbol)
            if control:  # False if unused key
                self.press_control(control)

        @self.window.event
        def on_key_release(symbol, modifiers=None):
            control = self.get_control(symbol)
            if control:  # False if unused key
                self.release_control(control)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            on_key_press(button, modifiers)
            self.reset_control(self.pause)

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            on_key_release(button, modifiers)

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.mouse_position = (x, y)

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.mouse_position = (x, y)

        @self.window.event
        def on_text(text):
            self.text += text

        @self.window.event
        def on_activate():
            self.reset_control(self.pause)

        @self.window.event
        def on_deactivate():
            # reset control state because inputs are no longer tracked until activated again
            self.reset()
            self.press_control(self.pause)

        @self.window.event
        def on_close():
            self.press_control(self.close)

        # Other possible actions: on_mouse_[action]
        # enter, leave, scroll, drag

        @self.window.event
        def on_move(x, y):
            self.reset()
            self.press_control(self.pause)

    def get_control(self, key):
        return self.key_to_control.get(key, False)

    def get_text(self):
        return self.text

    def get_key_set(self, control):
        return self.control_to_key_set.get(control, False)

    def update(self):
        self.text = ""
        for control in self.control_pressed:
            self.control_pressed[control] = 0

    def reset(self):
        self.update()
        for control in self.control_held_down:
            self.reset_control(control)

    def press_control(self, control):
        self.control_held_down[control] = self.control_held_down.get(control, 0) + 1
        self.control_pressed[control] = 1

    def release_control(self, control):
        self.control_held_down[control] = max(0, self.control_held_down.get(control, 0)-1)

    def reset_control(self, control):
        self.control_held_down[control] = 0
        self.control_pressed[control] = 0

    def is_control_pressed(self, control):
        return self.control_pressed.get(control, 0) > 0

    def is_control_held_down(self, control):
        return self.control_held_down.get(control, 0) > 0
