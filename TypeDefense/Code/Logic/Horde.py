from Code.Util.Text import Text
from Code.Logic.Line import Line


class Horde:
    def __init__(self, enemies, level, line_generator):
        self.level = level
        self.enemies: list
        self.enemies = enemies
        for e in self.enemies:
            e.horde = self
        self.lineGenerator = line_generator
        self.leader = None
        self.target = None
        self.target_line = None
        self.damage_count = 0
        self.set_target()

    def set_target(self, line=None):
        if len(self.enemies) == 0:
            self.remove()
            return
        self.leader = self.enemies[0]
        creature = self.leader.get_creature()
        if line is None:
            line = self.lineGenerator.generate_line(creature)
            self.target_line = line
        self.leader.set_tag(Text(line, -100, -100, self.level.batch))
        self.target = Line(line, self.leader)

    def damage_enemy(self, damage):
        enemy = damage.target
        self.damage_count += damage.value
        if enemy in self.enemies:
            if enemy.health <= self.damage_count:
                self.damage_count -= enemy.health
                self.remove_enemy(enemy, transfer=True)
                enemy.remove()

    def remove(self):
        self.level.remove_horde(self)

    def remove_enemy(self, enemy, transfer=False):
        self.enemies.remove(enemy)
        if self.leader == enemy:
            if transfer:
                self.target.remove()
                self.set_target(self.target_line)
            else:
                self.set_target()
