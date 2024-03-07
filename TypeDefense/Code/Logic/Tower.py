from Code.Logic.Entity import Entity
from Code.Logic.Projectile import Projectile
from Code.Logic.Damage import Damage
from Code.Util import Assets
#from Code.Util.Settings import Settings


class Tower(Entity):
    def __init__(self, *args,
                 level=None, attack_delay=1, damage_value=2, t_range=2.5,
                 damage_type=Damage.Projectile, projectile=Assets.Projectile.BallElemental, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = level
        self.attack_delay = attack_delay
        self.damage_type = damage_type
        self.projectile = projectile
        self.damage_value = damage_value
        self.charge = attack_delay
        self.range = t_range

    def get_projectile_position(self):
        return self.get_center()

    def shoot(self):
        target = self.get_target()
        if target is None:
            return

        self.charge = 0
        damage = Damage(self, target, self.damage_value, self.damage_type)
        x, y = self.get_projectile_position()
        Projectile(self.projectile, self.batch, self.camera, damage=damage, level=self.level, x=x, y=y)

    def get_target(self):
        x, y = self.get_center()
        target = None
        for horde in self.level.hordes:
            for enemy in horde.enemies:
                xe, ye = enemy.get_center()
                if (x-xe)**2 + (y-ye)**2 <= self.range:
                    target = enemy
                    if target.horde.leader is not target:
                        return target

        return target

    def update_shooting(self, dt):
        self.charge = min(self.attack_delay, self.charge+dt)
        if self.charge >= self.attack_delay:
            self.shoot()

    def upgrade(self):
        print("Tower upgrading")

    def update(self, dt):
        if not self.update_shooting(dt):
            return

        # move to next node
        super().update(dt)
