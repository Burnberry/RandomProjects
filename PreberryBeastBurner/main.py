from pyglet import window, clock, image, graphics
from PIL import Image

from Code.GameLogic import GameLogic
from Code.Camera import Camera
from Code.Entities import *
from Code.Logic.ActionType import ActionType
from Code.Logic.Index import Index
from Code.Logic.Actions.ActionSequence import ActionSequence
from Code.Logic.Actions.BaseAttackAction import BaseAttackAction
from Code.Logic.Actions.MoveAction import MoveAction

class Game:
	def __init__(self):
		# Window start
		self.setup_screen()

		self.loadSprites()

		# Game state
		self.frame = 0
		self.turn_states()
		self.turnState = self.STATE_SELECT
		# self.currentHUD = self.buttons
		self.currentHUD = []
		self.tilesHighlighted = []
		self.tilesHighlightedCoords = []
		self.highlightColor = self.BLACK
		self.tileHovered = None
		self.overlayHighlighted = None
		self.tile_actions = dict()

		# game logic
		self.entityGen = EntityGen(self.sprite_images, self.batch, [self.groupEntities], self.cam, self.scale, self.tileOffset)
		self.gameLogic = GameLogic(self.entityGen)
		self.gameLogic.init()
		self.gameLogic.restart()

		# load tiles
		area = self.gameLogic.area

		self.tileGrid = [[GameObject(self.sprite_images[area.getTile(x, y).sprite], self.batch, self.groupTiles, self.scale,
									 x * self.tileOffset, y * self.tileOffset) for y in range(self.cam.y, self.cam.y + self.cam.h)]
			for x in range(self.cam.x, self.cam.x + self.cam.w)]

		self.resetInputStates()
		self.base_tile_highlight()

		self.gameLogic.render()

	def setup_screen(self):
		self.screenWidth, self.screenHeight = 16*80, 9*80
		self.screen = window.Window(width=self.screenWidth, height=self.screenHeight)

		self.scale = 4
		self.tileOffset = 16 * self.scale
		self.cam = Camera(0, 0, self.screenWidth, self.screenHeight, self.tileOffset)

		@self.screen.event
		def on_mouse_press(x, y, button, modifiers):
			self.mouse_pressed(x, y, button, modifiers)

		@self.screen.event
		def on_mouse_release(x, y, button, modifiers):
			self.mouse_released(x, y, button, modifiers)

		@self.screen.event
		def on_mouse_motion(x, y, dx, dy):
			self.mouse_motion(x, y, dx, dy)

		@self.screen.event
		def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
			self.mouse_motion(x, y, dx, dy, 1 & buttons)
	def mouse_pressed(self, x, y, button, modifiers):
		if button != 1:
			return

		self.clickHeld = True
		self.clickPos = (x//self.tileOffset, y//self.tileOffset)
		self.clickPosExact = (x, y)

	def mouse_released(self, x, y, button, modifiers):
		if button != 1:
			return

		self.clickHeld = False

		# print(x, y, button, modifiers)
		for button in self.currentHUD:
			if self.collision(x, y, button):
				inst = button.instruction
				if inst == self.MOVE:
					self.move_pressed()
				# print("Move")
				elif inst == self.ATTACk:
					self.attack_pressed()
				# print("attack")
				else:
					print("Unhandled button:", inst)
				return

		x //= self.tileOffset
		y //= self.tileOffset
		if self.cam.w <= x or self.cam.h <= y:
			return

		tile = self.tileHighlightGrid[x][y]
		if tile in self.tilesHighlighted:
			self.select_tile(x, y)
			return
		return

	def attack_pressed(self):
		self.turnState = self.STATE_ATTACK
		self.unhighlight_tiles()
		tiles = self.gameLogic.getAttackTiles(self.gameLogic.player)
		self.tilesHighlightedCoords = tiles
		self.highlightColor = self.RED
		self.highlight_tiles(tiles, self.RED)
	def move_pressed(self):
		self.turnState = self.STATE_MOVE
		self.unhighlight_tiles()
		tiles = self.gameLogic.getMoveTiles(self.gameLogic.player)
		self.tilesHighlightedCoords = tiles
		self.highlightColor = self.YELLOW
		self.highlight_tiles(tiles, self.YELLOW)

	def mouse_motion(self, x, y, dx, dy, held=False):
		# Check camera movement first, then tile highlight
		x //= self.tileOffset
		y //= self.tileOffset
		if held:
			if (x, y) != self.clickPos:  # move camera
				xClick, yClick = self.clickPos
				dxCam, dyCam = xClick - x, yClick - y
				self.clickPos = (x, y)
				#print("move cam:", dxCam, dyCam)
				self.move_camera(dxCam, dyCam)

		# tile highlight
		for button in self.currentHUD:
			if self.collision(x, y, button):
				if self.tileHovered is not None:
					self.tileHovered.sprite.color = self.tileHovered.color
					self.tileHovered = None
				return

		if self.cam.w <= x or self.cam.h <= y:
			if self.tileHovered is not None:
				self.tileHovered.sprite.color = self.tileHovered.color
				self.tileHovered = None
			return

		if self.tileHovered is None:
			self.tileHovered = self.tileHighlightGrid[x][y]
			self.tileHovered.sprite.color = self.WHITE
			return

		if self.tileHovered != self.tileHighlightGrid[x][y]:
			self.tileHovered.sprite.color = self.tileHovered.color
			self.tileHovered = self.tileHighlightGrid[x][y]
			self.tileHovered.sprite.color = self.WHITE
			return

	def move_camera(self, dx, dy):
		xOld, yOld = self.cam.x, self.cam.y
		x, y = xOld + dx, yOld + dy

		# Avoid cam going out of area
		if not self.gameLogic.area.inside_area(x, 0):
			x = 0
			dx = x - xOld

		if not self.gameLogic.area.inside_area(0, y):
			y = 0
			dy = y - yOld

		if not self.gameLogic.area.inside_area(x + self.cam.w, 0):
			x = self.gameLogic.area.width - self.cam.w
			dx = x - xOld

		if not self.gameLogic.area.inside_area(0, y + self.cam.h):
			y = self.gameLogic.area.height - self.cam.h
			dy = y - yOld

		if (x, y) != (xOld, yOld):	# Move camera
			self.cam.x, self.cam.y = x, y

			# TileGrid
			self.setTileGrid()

			# Tile highlighting
			self.base_tile_highlight()

			# Sprites
			xMin, yMin = min(x, xOld), min(y, yOld)
			xMax, yMax = xMin + self.cam.w + abs(dx), yMin + self.cam.h + abs(dy)
			for xTile in range(xMin, xMax):
				for yTile in range(yMin, yMax):
					e = self.gameLogic.area.getTile(xTile, yTile).entity
					if e is not None:
						if self.cam.inside(xTile, yTile):  # Inside cam
							# Move entity and set visible
							xNew, yNew = (xTile - self.cam.x)*self.tileOffset, (yTile - self.cam.y)*self.tileOffset
							e.gameObject.set_position(xNew, yNew)
							e.set_visibility(True)
						else: # Outside cam
							# Set entity invisible
							e.set_visibility(False)
	def setTileGrid(self):
		for x in range(self.cam.w):
			for y in range(self.cam.h):
				tile = self.tileGrid[x][y]
				newImage = self.sprite_images[self.gameLogic.area.getTile(x + self.cam.x, y + self.cam.y).sprite]
				if tile.sprite.image is not newImage:
					tile.sprite.image = newImage


	def base_tile_highlight(self):
		self.unhighlight_tiles()
		actions = self.gameLogic.player.AI.get_basic_actions()
		self.tile_actions = dict()
		attack_tiles = []
		move_tiles = []

		for action in actions:
			a = action
			if isinstance(action, ActionSequence):
				a = action.actions[-1]
			tile = (a.x, a.y)

			if a.tag == ActionType.MOVE:
				move_tiles.append(tile)
			elif a.tag == ActionType.ATTACK:
				attack_tiles.append(tile)
			else:
				raise Exception("ERROR, unhandled action type")

			self.tile_actions[tile] = action

		self.highlight_tiles(move_tiles, self.YELLOW)
		self.highlight_tiles(attack_tiles, self.RED)


	def highlight_tiles(self, tiles, color):
		for x, y in tiles:
			x_cam = x - self.cam.x
			y_cam = y - self.cam.y
			if self.cam.inside(x, y):
				tile = self.tileHighlightGrid[x_cam][y_cam]
				self.tilesHighlighted.append(tile)
				#print(x, y, self.cam.w, self.cam.h)
				if tile.color != color:
					#print("coloring")
					tile.color = color
					if tile != self.tileHovered:
						tile.sprite.color = color

	def unhighlight_tiles(self):
		for tile in self.tilesHighlighted:
			tile.color = self.BLACK
			if tile != self.tileHovered:
				tile.sprite.color = self.BLACK
		self.tilesHighlighted = []

	def select_tile(self, x, y):
		e = self.gameLogic.player
		action = self.tile_actions[(x+self.cam.x, y+self.cam.y)]
		if action.tag == ActionType.ATTACK:
			self.gameLogic.action(e, ActionType.ATTACK, x + self.cam.x, y + self.cam.y)
		elif action.tag == ActionType.MOVE:
			if isinstance(action, ActionSequence):
				actions = action.actions
			else:
				actions = [action]
			for move_action in actions:
				self.gameLogic.action(e, ActionType.MOVE, move_action.x, move_action.y)
		else:
			print("ERROR, unhandled tile select state:", self.turnState)
			return

		self.base_tile_highlight()
		if len(self.tile_actions) == 0:  # No possible action
			if self.gameLogic.player.AP + self.gameLogic.player.MP > 0: # Need to end turn
				self.gameLogic.action(e, ActionType.END_TURN, 0, 0)
			self.gameLogic.finish_group_turn()
			self.base_tile_highlight()

		self.gameLogic.render()


		#self.currentHUD = self.buttons
		#for button in self.buttons:
		#	button.sprite.visible = True

	def loadImage(self, path):
		im = Image.open(path)
		w, h = im.size
		w *= self.scale
		h *= self.scale

		im = im.resize((w, h), Image.Resampling.NEAREST)
		im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
		return image.ImageData(w, h, im.mode, im.tobytes())

	def turn_states(self):
		self.STATE_SELECT = 0
		self.STATE_MOVE = 1
		self.STATE_ATTACK = 2
	def loadSprites(self):
		# Create groups
		self.groupBackround = graphics.OrderedGroup(0)
		self.groupTiles = graphics.OrderedGroup(10)
		self.groupTileHighlight = graphics.OrderedGroup(20)
		self.groupEntities = graphics.OrderedGroup(30)
		self.groupOverlay = graphics.OrderedGroup(40)
		self.groupButtons = graphics.OrderedGroup(50)

		# Sprites in batch will be drawn
		self.batch = graphics.Batch()

		# Overlay stuff
		# Tile edges
		# tileHighlightImage = self.loadImage("Assets/Overlay/tileOverlayWhite.png")
		tileHighlightImage = self.loadImage(Index.filepath[Index.Overlay.tile_overlay_white])
		alpha = 128
		self.tileHighlightGrid = [[GameObject(tileHighlightImage, self.batch, self.groupTileHighlight, self.scale, x=x*self.tileOffset, y=y*self.tileOffset, alpha=alpha) for y in range(self.cam.h)] for x in range(self.cam.w)]
		self.colors()
		for row in self.tileHighlightGrid:
			for tile in row:
				tile.sprite.color = self.BLACK
		# buttons
		self.gameInstructions()
		#self.moveButton = GameObject(self.loadImage("Assets/Overlay/MoveButton.png"), self.batch, self.groupButtons, self.scale, dy=0, x=2*self.tileOffset, inst=self.MOVE)
		#self.attackButton = GameObject(self.loadImage("Assets/Overlay/AttackButton.png"), self.batch, self.groupButtons, self.scale, dy=0, x=5*self.tileOffset, inst=self.ATTACk)

		#self.buttons = [self.moveButton, self.attackButton]
		#for b in self.buttons:
		#	b.sprite.visible = False

		# Sprites
		self.sprite_images = {}
		for index in Index.filepath.keys():
			img = self.loadImage(Index.filepath[index])
			self.sprite_images[index] = img
	def gameInstructions(self):
		self.ATTACk = 0
		self.MOVE = 1

	def colors(self):
		self.BLACK = (0, 0, 0)
		self.WHITE = (255, 255, 255)
		self.RED = (255, 0, 0)
		self.YELLOW = (255, 255, 0)
	def resetInputStates(self):
		self.clickHeld = False
		self.clickPos = (0, 0)

	def collision(self, x, y, obj):
		xo, yo, w, h = obj.sprite.x, obj.sprite.y, obj.sprite.width, obj.sprite.height
		return xo <= x < xo + w and yo <= y < yo + h

	def render(self):

		_ = self.screen.dispatch_events()
		_ = self.screen.dispatch_event('on_draw')
		# Draw screen
		# Order: Clear screen, draw tiles + overlay, draw entities, draw hud
		self.screen.clear()
		self.batch.draw()
		self.screen.flip()

	def run(self):
		#print("Starting loop")
		while(True):
			#print(self.frame)
			self.frame += 1
			#self.resetInputStates()
			_ = clock.tick()
			print(clock.get_fps())

			self.render()


game = Game()
game.run()