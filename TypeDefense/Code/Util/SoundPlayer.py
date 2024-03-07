from pyglet import media

from Code.Util import Assets


class SoundPlayer:
    _audio = media.Player()
    _audio.volume = 0
    _sound = Assets.get_sound(Assets.Sound.Knock)
    _audio.queue(Assets.get_sound(Assets.Sound.Knock))
    _audio.play()

    def __init__(self, camera):
        self.camera = camera

    def play_sound(self, sound, x, y):
        audio = media.Player()
        x, y = self.transform_coordinates(x, y)
        audio.position = (x, y, 0)
        audio.queue(sound)
        audio.play()
        return audio

    def transform_coordinates(self, x, y):
        scale = 5

        #cx, cy = self.camera.get_center()
        #x, y = x-cx, y-cy
        #x, y = x/scale, y/scale
        return x, y
