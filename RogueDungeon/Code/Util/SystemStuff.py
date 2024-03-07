from pyglet import canvas


class SystemStuff:
    @staticmethod
    def getDefaultScreenResolution():
        """
        :return: width, height
        """
        display = canvas.Display()
        screen = display.get_default_screen()
        return screen.width, screen.height
