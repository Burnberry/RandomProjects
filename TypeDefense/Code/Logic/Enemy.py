from Code.Logic.Entity import Entity
from Code.Util.Settings import Settings


class Enemy(Entity):
    def __init__(self, *args, health=3, speed=5, path=None, node_offset=(0, 0), level=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = level
        self.health = health
        self.speed = speed
        self.path = path
        self.node_offset = node_offset
        self.node = self.path.start
        self.damage_received = 0
        self.horde = None

        x, y = self.path.start.position
        dx, dy = self.node_offset
        x, y = x+dx, y+dy
        if self.path:
            self.set_position(x, y)

    def get_creature(self):
        return self.asset_index

    def hit(self):
        self.horde.remove_enemy(self)
        self.remove()

    def get_node_position(self, node):
        x, y = node.position
        dx, dy = self.node_offset
        return x+dx, y+dy

    def update_movement(self, dt):
        movement = dt * self.speed * Settings.SpeedFactor

        while True:
            node1 = self.node.child

            x0, y0 = self.x, self.y
            x1, y1 = self.get_node_position(node1)
            dx, dy = x1-x0, y1-y0
            if movement*abs(movement) >= dx**2 + dy**2:  # support -dt, so abs()
                movement -= (dx**2 + dy**2)**0.5
                self.node = self.node.child
                self.set_position(*self.get_node_position(self.node))
                if self.node.child is None:
                    self.level.reached_destination(self)
                    return False
            else:
                break

        # movement vector
        c = (dx**2 + dy**2)**0.5
        dx, dy = movement*dx/c, movement*dy/c
        self.set_position(x0+dx, y0+dy)
        return True

    def update(self, dt):
        if not self.update_movement(dt):
            return

        # move to next node
        super().update(dt)
