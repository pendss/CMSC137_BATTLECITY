import pygame as pg

from sprites import *
from animation import *
from settings import *

blueTank = [BLUE_UP, BLUE_DOWN, BLUE_LEFT, BLUE_RIGHT]
redTank = [RED_UP, RED_DOWN, RED_LEFT, RED_RIGHT]
# greenTank = [GREEN_UP, GREEN_DOWN, GREEN_LEFT, GREEN_RIGHT]
# orangeTank = [ORANGE_UP, ORANGE_DOWN, ORANGE_LEFT, ORANGE_RIGHT]

class Player(pg.sprite.Sprite):
	def __init__(self, game, name, pos, health, color):
		pg.sprite.Sprite.__init__(self)

		# self.curr_player = curr_player
		self.name = name
		# self.status = status
		self.health = health
		self.pos = pos
		# self.move = move
		self.color = color       	

		self.game = game
		if self.color == 'blue':
			self.image = blueTank[0]
		elif self.color == 'red':
			self.image = redTank[1]
		elif self.color == 'green':
			self.image = greenTank[2]
		elif self.color == 'orange':
			self.image = orangeTank[3]

		self.rect = self.image.get_rect()   
		self.vel = vec(0,0)
		self.acc = vec(0,0)

	def update(self):
		self.acc = vec(0, 0)
		keys = pg.key.get_pressed()

		# collision = pg.sprite.spritecollide(self, self.game.bricks, False)
		# for brick in collision:
		# if not collision:
		if keys[pg.K_w]:
			self.acc.y = -PLAYER_ACC
			if self.color == 'blue':
				self.image = blueTank[0]
			elif self.color == 'red':
				self.image = redTank[0]
			elif self.color == 'green':
				self.image = greenTank[0]
			elif self.color == 'orange':
				self.image = orangeTank[0]
		elif keys[pg.K_s]:
			self.acc.y = PLAYER_ACC
			if self.color == 'blue':
				self.image = blueTank[1]
			elif self.color == 'red':
				self.image = redTank[1]
			elif self.color == 'green':
				self.image = greenTank[1]
			elif self.color == 'orange':
				self.image = orangeTank[1]
		elif keys[pg.K_a]:
			self.acc.x = -PLAYER_ACC
			if self.color == 'blue':
				self.image = blueTank[2]
			elif self.color == 'red':
				self.image = redTank[2]
			elif self.color == 'green':
				self.image = greenTank[2]
			elif self.color == 'orange':
				self.image = orangeTank[2]
		elif keys[pg.K_d]:
			self.acc.x = PLAYER_ACC
			if self.color == 'blue':
				self.image = blueTank[3]
			elif self.color == 'red':
				self.image = redTank[3]
			elif self.color == 'green':
				self.image = greenTank[3]
			elif self.color == 'orange':
				self.image = orangeTank[3]

		# apply friction
		self.acc += self.vel * PLAYER_FRICTION
		# equations of motion
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		# wrap around the sides of the screen
		if self.pos.x > WIDTH-350 and self.pos.y > HEIGHT-50:
		    self.pos.x = 0
		    self.pos.y = 0

		if self.pos.x < 0 and self.pos.y < 0 :
		    self.pos.x = WIDTH-350
		    self.pos.y = HEIGHT-50


		self.rect = self.pos