from Code.Util.GameObject import BaseButton, TextGameObject, SpriteGameObject


class ButtonText(BaseButton):
    def __init__(self, scene, x, y, anchor, text, f, args=None, group=TextGameObject.Group.Text):
        obj = TextGameObject(scene, x, y, group, anchor, text)
        super().__init__(obj, f, args)


class ButtonSprite(BaseButton):
    def __init__(self, scene, x, y, anchor, asset, f, args=None, group=SpriteGameObject.Group.Foreground):
        obj = SpriteGameObject(scene, x, y, group, anchor, asset)
        super().__init__(obj, f, args)
