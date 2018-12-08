# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2

up = pg.image.load('./sprites/tankBlueUp.png')
down = pg.image.load('./sprites/tankBlueDown.png')
left = pg.image.load('./sprites/tankBlueLeft.png')
right = pg.image.load('./sprites/tankBlueRight.png')
wall = pg.image.load("./sprites/wall.png")
class Player(pg.sprite.Sprite):
    def __init__(self,game, name,pos,move,health):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = up
        self.name = name
        self.pos = pos
        self.move = move
        self.health = health
        self.rect = self.image.get_rect()

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()

        # collision = pg.sprite.spritecollide(self, self.game.bricks, False)
        # if not collision:

        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            self.image = left
        elif keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
            self.image = right
        elif keys[pg.K_w]:
            self.acc.y = -PLAYER_ACC
            self.image =  up
        elif keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
            self.image = down

        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect = self.pos

class Brick(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = wall
        self.rect = self.image.get_rect()

    def update(self):
        self.rect = self.pos