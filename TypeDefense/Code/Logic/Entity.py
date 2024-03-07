from Code.Util.GameObject import GameObject


# Game object class which adds movement to object, requires update(dt) call each frame
class Entity(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vx, self.vy = 0, 0

    def update(self, dt):
        dx, dy = self.vx*dt, self.vy*dt
        self.move(dx, dy)
        super().update(dt)

    def set_speed(self, vx, vy):
        self.vx, self.vy = vx, vy
