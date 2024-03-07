from Code.Logic.Path import Path
from Code.Logic.GameMap import GameMap
from Code.Util import Assets
from Code.Util.Iter import Iter
from Code.Logic.Line import Line
from Code.Util.GameObject import GameObject
from Code.Logic.Enemy import Enemy
from Code.Logic.Tower import Tower
from Code.Logic.Horde import Horde
from numpy.random import randint, random
from Code.Util.Text import Text
from Code.Util.Settings import Settings

from Code.Maps.MapMaker import *


class Level:
    # states
    stateBattle = Iter.i()
    stateBuild = Iter.i()
    stateFinish = Iter.i()

    def __init__(self, game):
        self.batch = game.batch
        self.camera = game.camera
        self.controller = game.controller
        self.player = game.player
        self.soundPlayer = game.soundPlayer
        self.lineGenerator = game.lineGenerator

        self.gameMap = test_map(self.batch, self.camera)

        # Player state stuff
        self.line = ""
        self.player_line = Text(self.line, self.camera.screenWidth // 2, 5, self.batch)

        # Game stuff
        self.time = 0
        self.gold = 0
        self.breaches = 0
        self.wave_count = 0
        self.castle = GameObject(Assets.Creature.Castle, self.batch, self.camera)
        # Get end of path and place castle
        pos = self.gameMap.paths[0].end.position
        self.castle.set_position(*pos)
        self.castle.set_tag(Text(self.breaches, -100, -100, self.batch))
        self.castle.sprite.scale *= 4
        self.hordes = []

        self.waves = []
        self.make_waves()

        self.wave = []
        self.horde_spawn = ()
        self.next_horde_time = 0
        self.hordes_spawning = True

        # game state
        self.state = self.stateBuild

        # UI stuff
        self.cursor_color = (255, 255, 0)
        self.cursor_opacity = 192
        self.cursor = GameObject(Assets.Overlay.tileOverlay, self.batch, self.camera, 8, 1,
                                 self.cursor_opacity, group=GameObject.UI)
        self.cursor.set_color(self.cursor_color)
        self.lineActions = []
        self.cursor.set_tag(Text("", 0, 0, self.batch))

        #self.to_battle_state()
        self.to_build_state()

    def start(self):
        pass

    def update(self, dt):
        self.time += dt
        if self.state == self.stateBattle:
            while self.time >= self.next_horde_time and self.hordes_spawning:
                self.spawn_horde()
            if not self.hordes_spawning and len(self.hordes) == 0:
                self.to_build_state()

    def handle_input(self):
        # line submitted
        if self.controller.is_control_pressed(self.controller.submit):
            if len(self.line) > 0:
                self.soundPlayer.play_sound(Assets.get_sound(Assets.Sound.Enter), 0, 0)
            self.submit(self.line)
            self.reset_line()

        if self.controller.is_control_held_down(self.controller.backspace):
            self.castle.sprite.rotation += 1

        if self.controller.is_control_pressed(self.controller.backspace):
            if len(self.line) > 0:
                self.line = self.line[:-1]

        self.add_text(self.controller.text)

        if self.state == self.stateBuild:
            self.handle_input_UI()

    def handle_input_UI(self):
        dx, dy = 0, 0
        control_checks = [(self.controller.up, 0, 1), (self.controller.down, 0, -1), (self.controller.left, -1, 0), (self.controller.right, 1, 0)]
        for control, x, y in control_checks:
            if self.controller.is_control_pressed(control):
                dx += x
                dy += y
        if dx != 0 or dy != 0:
            self.move_cursor(dx, dy)

    def move_cursor(self, dx, dy):
        self.cursor.move(dx, dy)
        x, y = self.cursor.get_position()
        tile = self.gameMap.get_tile(x, y)
        self.lineActions = []
        if tile.tile_type == tile.default:
            self.lineActions.append("build tower")
        if tile.tile_type == tile.tower:
            self.lineActions.append("upgrade tower")
        self.lineActions.append("next wave")

        self.update_line_actions()

    def update_line_actions(self):
        txt = ""
        for action in self.lineActions:
            txt += action + ' | '
        txt = txt[:-3]
        self.cursor.tag.set_text(txt)

    def submit(self, line):
        if Line.submit_line(line):
            self.gold += 1

        if self.stateBuild:
            self.checkLineAction(line)

    def checkLineAction(self, line):
        if line not in self.lineActions:
            return
        x, y = self.cursor.get_position()
        if line == "build tower":
            self.build_tower(x, y)
        if line == "upgrade tower":
            tile = self.gameMap.get_tile(x, y)
            tower = tile.child
            tower.upgrade()
        if line == "next wave":
            self.to_battle_state()

    def to_build_state(self):
        self.state = self.stateBuild
        Line.reset()
        self.cursor.set_visible(True)
        self.move_cursor(0, 0)
        self.wave_count += 1
        print("Prepare for wave", self.wave_count)

    def to_battle_state(self):
        self.state = self.stateBattle
        self.time = 0
        self.cursor.set_visible(False)

        self.wave = self.waves.pop(0)
        self.horde_spawn = self.wave.pop(0)
        _, time, delay = self.horde_spawn
        self.next_horde_time = time
        self.hordes_spawning = True

    def build_tower(self, x, y):
        tile = self.gameMap.get_tile(x, y)
        tile.set_tile_type(tile.tower)
        tower = Tower(Assets.Tower.TowerDefault, self.batch, self.camera, level=self, x=x, y=y)
        tile.set_child(tower)

    def reset_line(self):
        self.line = ""
        self.controller.text = ""  # Don't count submission key as text (ignore enter text for example)
        self.player_line.set_text(self.line)

    def add_text(self, text):
        if len(text) > 0:
            self.line += text
            self.soundPlayer.play_sound(Assets.get_sound(Assets.Sound.Key), 0, 0)
        self.player_line.set_text(self.line)

    def spawn_horde(self):
        enemies, time, delay = self.horde_spawn
        self.next_horde_time = time
        dt = -delay
        enemy_objs = []
        for i, creature in enumerate(enemies):
            e = self.spawn_enemy(creature, i * dt)
            enemy_objs.append(e)
        horde = Horde(enemy_objs, self, self.lineGenerator)
        self.hordes.append(horde)

        if len(self.wave) == 0:
            self.hordes_spawning = False
        else:
            self.horde_spawn = self.wave.pop(0)
            _, time, _ = self.horde_spawn
            self.next_horde_time = time

    def remove_horde(self, horde):
        self.hordes.remove(horde)

    def spawn_enemy(self, creature, dt=0.0):
        pth = self.gameMap.paths[0]

        node_offset = (0.8*(random()-0.5), 0.1 + 0.8*random())
        e = Enemy(creature, self.batch, self.camera, path=pth, node_offset=node_offset, level=self)
        e.update_movement(dt)

        return e

    def reached_destination(self, enemy):
        enemy.remove()
        enemy.horde.remove_enemy(enemy, transfer=True)
        self.breaches += 1
        self.castle.tag.set_text(self.breaches)

    def make_waves(self):
        self.waves = []

        # wave 1
        wave = []
        time = 0

        creature = Assets.Creature.Peasant0
        enemy_delay = 0.5
        enemies = [creature for _ in range(1)]
        horde_spawn = (enemies, time, enemy_delay)
        time += enemy_delay*len(enemies)
        wave.append(horde_spawn)

        time += 4
        enemies = [creature for _ in range(2)]
        horde_spawn = (enemies, time, enemy_delay)
        time += enemy_delay * len(enemies)
        wave.append(horde_spawn)

        time += 2
        enemies = [creature for _ in range(4)]
        horde_spawn = (enemies, time, enemy_delay)
        time += enemy_delay * len(enemies)
        wave.append(horde_spawn)

        time += 5
        enemies = [creature for _ in range(10)]
        horde_spawn = (enemies, time, enemy_delay)
        time += enemy_delay * len(enemies)
        wave.append(horde_spawn)

        self.waves.append(wave)

        for i in range(4, 50):

            # wave 2
            wave = []
            time = 0

            creature = Assets.Creature.Peasant0
            enemy_delay = 0.5
            enemies = [creature for _ in range(5)]
            horde_spawn = (enemies, time, enemy_delay)
            time += enemy_delay * len(enemies)
            wave.append(horde_spawn)

            for j in range(i):
                time += 2 + j/2
                n = ((1 + j/6)*i)**1.2
                enemies = [creature for _ in range(int(n))]
                horde_spawn = (enemies, time, enemy_delay)
                time += enemy_delay * len(enemies)
                wave.append(horde_spawn)

            self.waves.append(wave)
