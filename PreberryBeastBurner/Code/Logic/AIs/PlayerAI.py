from Code.Logic.AIs.BaseAI import BaseAI


class PlayerAI(BaseAI):
    def __init__(self, entity, area, gamelogic):
        super().__init__(entity, area, gamelogic)

    def do_action(self):
        print("Player", self.Entity.tag, "should be controlled by player")
        return
