from Code.GameObject import GameObject
from Code.Logic.Index import Index

class EntityGen:
    count = 0
    def __init__(self, images, batch, groups, cam, scale, tile_offset):
        self.loadedImages = images
        self.batch = batch
        self.groups = groups
        self.camera = cam
        self.scale = scale
        self.tileOffset = tile_offset

        self.entities = []

        self.gameLogic = None # set by gameLogic


    def move_entity(self, entity, x, y):
        x_cam, y_cam = x - self.camera.x, y - self.camera.y
        if self.camera.inside(x, y):
            entity.gameObject.set_position(x_cam*self.tileOffset, y_cam*self.tileOffset)
            entity.set_visibility(True)
        else:
            entity.set_visibility(False)
    def remove_entity(self, entity):
        self.entities.remove(entity)
        entity.gameObject.remove()

    def create(self, entity):
        e = GameObject(self.loadedImages[entity.spriteIndex], self.batch, self.groups[0], self.scale,
                       entity.x * self.tileOffset, entity.y * self.tileOffset)
        # set position and visibility correct
        x, y = entity.x, entity.y
        x_cam, y_cam = x - self.camera.x, y - self.camera.y
        if self.camera.inside(x, y):
            e.set_position(x_cam * self.tileOffset, y_cam * self.tileOffset)
            e.sprite.visible = True
        else:
            e.sprite.visible = False
        self.entities.append(entity)
        return e

    class Entity:
        def __init__(self, x, y, area, sprite_index=1, gen=None, control=1):
            EntityGen.count = EntityGen.count + 1

            self.x, self.y = x, y
            self.control = control
            self.spriteIndex = sprite_index
            self.gen = gen
            self.gameLogic = self.gen.gameLogic

            self.area = area
            self.AI = None  # Set by gameLogic if required
            # Creature stats
            self.maxAP = 0
            self.maxMP = 0
            self.AP = 0
            self.MP = 0
            self.damage = 0
            self.Alive = True

            self.gameObject = self.gen.create(self)

        def show(self):
            return self.spriteIndex

        def move(self, x, y):
            self.x, self.y = x, y

            if self.gameObject:
                self.gen.move_entity(self, x, y)

        def remove(self):
            self.gen.remove_entity(self)

        def set_visibility(self, visible):
            if self.gameObject.sprite.visible != visible:
                self.gameObject.sprite.visible = visible

    class Player(Entity):
        def __init__(self, x, y, area, sprite=Index.Creature.player, health=10, damage=2, gen=None, control=1):
            super().__init__(x, y, area, sprite, gen, control)
            EntityGen.count = EntityGen.count - 1
            self.tag = "player"
            self.health = health
            self.damage = damage
            self.lvl = 1
            self.expNeeded = 2

            self.maxMP = 1
            self.maxAP = 1

        def gain_exp(self, exp):
            self.expNeeded -= exp
            while self.expNeeded <= 0:
                self.level_up()

        def level_up(self):
            self.lvl += 1
            self.health += 3 + self.lvl//2
            self.damage += 1
            if self.lvl % 5 == 2:
                self.maxMP += 1
            if self.lvl % 7 == 4:
                self.maxAP += 1
                self.damage -= 2

            self.expNeeded += self.lvl**2 - 3*self.lvl + 5

    class Rat(Entity):
        def __init__(self, x, y, area, sprite=Index.Creature.rat, health=3, damage=1, gen=None, control=1):
            super().__init__(x, y, area, sprite, gen, control)
            self.tag = "Rat " + str(EntityGen.count)

            self.health = health
            self.damage = damage

            self.maxMP = 1
            self.maxAP = 1

    class Bat(Entity):
        def __init__(self, x, y, area, sprite=Index.Creature.bat, health=5, damage=1, gen=None, control=1):
            super().__init__(x, y, area, sprite, gen, control)
            self.tag = "Bat " + str(EntityGen.count)

            self.health = health
            self.damage = damage

            self.maxMP = 2
            self.maxAP = 1

    class Spider(Entity):
        def __init__(self, x, y, area, sprite=Index.Creature.spider, health=9, damage=2, gen=None, control=1):
            super().__init__(x, y, area, sprite, gen, control)
            self.tag = "Spider " + str(EntityGen.count)

            self.health = health
            self.damage = damage

            self.maxMP = 1
            self.maxAP = 1

    class Wolf(Entity):
        def __init__(self, x, y, area, sprite=Index.Creature.wolf, health=16, damage=3, gen=None, control=1):
            super().__init__(x, y, area, sprite, gen, control)
            self.tag = "Wolf " + str(EntityGen.count)

            self.health = health
            self.damage = damage

            self.maxMP = 2
            self.maxAP = 1
