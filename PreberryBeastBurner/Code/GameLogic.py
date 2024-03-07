import os
from random import randint

from Code.Logic.Area import Area
from Code.Logic.Battle import Battle
from Code.Logic.ActionType import ActionType
from Code.Logic.Index import Index
from Code.Logic.AIs.BaseAI import BaseAI
from Code.Logic.AIs.PlayerAI import PlayerAI
from Code.Utils.Distance import *


class GameLogic:
	def __init__(self, entity_gen):
		# map
		self.area = Area(25, 15)

		# entities
		self.entityGen = entity_gen
		self.entities = []
		self.player = None
		self.battle = None

		# Render dict
		self.draw = {
			Index.Tile.grass: '.',
			Index.Tile.rock: '.',
			Index.Creature.player: 'P',
			Index.Creature.rat: 'R',
			Index.Creature.spider: 'S',
			Index.Creature.bat: 'B',
			Index.Creature.wolf: 'W'
		}

		# Game state
		self.round = 0
		self.level = 0
		self.entitiesInBattle = None
		self.entitiesActive = None

	def init(self):
		self.entityGen.gameLogic = self

	def restart(self):
		# entities
		while len(self.entities) > 0:
			self.removeEntity(self.entities[0])
		self.player = self.entityGen.Player(0, 0, self.area, gen=self.entityGen, control=0)
		self.player.AI = PlayerAI(self.player, self.area, self)
		self.entities.append(self.player)
		self.battle = Battle([e for e in self.entities])
		self.area.getTile(0, 0).entity = self.player
		self.level = 0
		self.spawn_wave()

		# Game state
		self.round = 0
		self.entitiesInBattle = [e for e in self.entities]
		self.entitiesActive = [self.entitiesInBattle[0]]

	def get_active_entities(self):
		return self.battle.control, self.battle.entitiesActive

	def next_action(self):
		control, active_entities = self.get_active_entities()
		if control == 1:
			# Only a single active entity implemented
			entity = active_entities[0]
			if not entity.AI.do_action():
				self.action(entity, ActionType.END_TURN, 0, 0)
			actions = []
			return actions
		else:
			# No more turns
			return False

	def next_action_parallel(self):
		# To implement
		return self.next_action()

	def finish_group_turn(self):
		actions = []
		while(self.battle.control == 1):
			actions += self.next_action()
		return

	def action(self, entity, move, x, y):
		dx, dy = x - entity.x, y - entity.y
		AP, MP = 0, 0
		if move == ActionType.MOVE:
			if self.validMove(entity, dx, dy):
				MP = abs(dx) + abs(dy)
				self.moveEntity(entity, dx, dy)
				self.battle.action(entity, AP, MP)
				return
		if move == ActionType.ATTACK:
			if self.area.inside_area(x, y):
				AP = 1
				self.attack(entity, x, y)
				self.battle.action(entity, AP, MP)
				return
		if move == ActionType.END_TURN:
			self.battle.end_turn(entity)
			return

		print("Error", "Unhandled move type in action", "move:", move)

	def render(self):
		os.system('cls')
		for row in self.area.field[::-1]:
			print("".join([self.draw.get(tile.show(), '.') for tile in row]))
		print(' '*(self.area.width+2))
		e = self.player
		print("player", "health", e.health, "lvl", e.lvl)
		offset = max(e.maxAP, e.maxMP)
		print("O" * e.AP + "." * (e.maxAP - e.AP), "Action Points")
		print("O" * e.MP + "." * (e.maxMP - e.MP), "Movement Points")
		print(" ")
		for i, e in enumerate(self.entities):
			if isinstance(e, self.entityGen.Player):
				continue
			print(e.tag, "health", e.health)

		# Debugging
		"""
		print("DEBUGGING")
		print(self.entityGen.entities)
		"""

	def moveEntity(self, entity, dx, dy):
		x, y = entity.x, entity.y
		self.area.getTile(x, y).entity = None
		self.area.getTile(x+dx, y+dy).entity = entity
		entity.move(x+dx, y+dy)

	def removeEntity(self, entity):
		tile = self.area.getTile(entity.x, entity.y)
		tile.entity = None
		self.entities.remove(entity)
		self.battle.remove(entity)
		entity.remove()

	def attack(self, entity, x, y):
		tile = self.area.getTile(x, y)
		target = tile.entity
		if target:
			print(target.tag, "attacked by", entity.tag, "for", entity.damage, "damage")
			target.health -= entity.damage
			if target.health <= 0:
				self.removeEntity(target)
				if isinstance(target, self.entityGen.Player):
					print("Player died")
					self.restart()
				else:
					self.player.gain_exp(1)
					if len(self.entities) == 1:
						self.spawn_wave()

	def validMove(self, entity, dx, dy):
		x, y = entity.x, entity.y
		if not self.area.inside_area(x+dx, y+dy): return False

		if self.area.getTile(x+dx, y+dy).getEntity():
			return False
		return True

	def getMoveTiles(self, entity):
		x, y = entity.x, entity.y
		tiles = []
		positions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
		for pos in positions:
			if self.area.inside_area(*pos):
				tiles.append(pos)
		return tiles

	def getAttackTiles(self, entity):
		x, y = entity.x, entity.y
		tiles = []
		for i in range(-1,2):
			for j in range(-1, 2):
				pos = (x+i, y+j)
				if self.area.inside_area(*pos):
					tiles.append(pos)
		return tiles

	def spawn_wave(self):
		print("Level", self.level)
		if self.level == 0:
			for i in range(3):
				self.spawn_creature(self.entityGen.Rat)
		elif self.level == 1:
			for i in range(2):
				self.spawn_creature(self.entityGen.Rat)
			for i in range(1):
				self.spawn_creature(self.entityGen.Bat)
		elif self.level == 2:
			for i in range(5):
				self.spawn_creature(self.entityGen.Rat)
			for i in range(1):
				self.spawn_creature(self.entityGen.Spider)
		elif self.level == 3:
			for i in range(7):
				self.spawn_creature(self.entityGen.Rat)
			for i in range(1):
				self.spawn_creature(self.entityGen.Spider)
			for i in range(2):
				self.spawn_creature(self.entityGen.Bat)
		elif self.level == 4:
			for i in range(11):
				self.spawn_creature(self.entityGen.Rat)
			for i in range(1):
				self.spawn_creature(self.entityGen.Spider)
			for i in range(4):
				self.spawn_creature(self.entityGen.Bat)
		elif self.level == 5:
			for i in range(11):
				self.spawn_creature(self.entityGen.Rat)
			for i in range(1):
				self.spawn_creature(self.entityGen.Wolf)
		elif self.level == 6:
			for i in range(12):
				self.spawn_creature(self.entityGen.Rat)
			for i in range(2):
				self.spawn_creature(self.entityGen.Spider)
			for i in range(4):
				self.spawn_creature(self.entityGen.Bat)
			for i in range(1):
				self.spawn_creature(self.entityGen.Wolf)
		else:
			for i in range(self.level):
				self.spawn_creature(self.entityGen.Rat)
			for i in range(self.level//3 + 1):
				self.spawn_creature(self.entityGen.Spider)
			for i in range(self.level//2 + 1):
				self.spawn_creature(self.entityGen.Bat)
			for i in range((self.level+2)//5 + 1):
				self.spawn_creature(self.entityGen.Wolf)

		self.level += 1


	def spawn_creature(self, creature):
		exit = False
		while(not exit):
			x = randint(0, self.area.width-1)
			y = randint(0, self.area.height-1)
			exit = True
			if rectilinear(self.player.x, self.player.y, x, y) <= 5:
				exit = False
			for entity in self.entities:
				if rectilinear(entity.x, entity.y, x, y) == 0:
					exit = False

		monster = creature(x, y, self.area, gen=self.entityGen)

		monster.AI = BaseAI(monster, self.area, self)
		self.entities.append(monster)
		self.area.getTile(x, y).entity = monster
		self.battle.add(monster)
