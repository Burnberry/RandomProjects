from Code.Logic.Entity import Entity
from Code.Util.Settings import Settings


class Projectile(Entity):
    def __init__(self, *args, level=None, damage=None, speed=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = level
        self.damage = damage
        self.speed = speed
        self.target = damage.target

    def update_movement(self, dt):
        movement = dt * self.speed * Settings.SpeedFactor

        x, y = self.get_position()
        x0, y0 = self.target.get_position()
        dx, dy = x0-x, y0-y
        distance = (dx**2 + dy**2)**0.5

        if distance <= movement:
            self.target.horde.damage_enemy(self.damage)
            self.remove()
            return False

        dx, dy = movement*dx/distance, movement*dy/distance
        self.set_position(x+dx, y+dy)
        return True

    def update(self, dt):
        if not self.update_movement(dt):
            return

        # move to next node
        super().update(dt)
