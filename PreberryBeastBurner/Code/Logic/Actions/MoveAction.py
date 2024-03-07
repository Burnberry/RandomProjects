from Code.Logic.Actions.Action import Action


class MoveAction(Action):
    def __init__(self, tag, entity, destination_x, destination_y):
        super().__init__(tag, entity)
        self.x = destination_x
        self.y = destination_y
