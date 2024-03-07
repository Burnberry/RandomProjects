from Code.Logic.Actions.Action import Action


class BaseAttackAction(Action):
    def __init__(self, tag, entity, target, x, y, damage):
        super().__init__(tag, entity)
        self.target = target    # Entity to attack, if None: use coordinates to target tile
        self.x = x
        self.y = y
        self.damage = damage
