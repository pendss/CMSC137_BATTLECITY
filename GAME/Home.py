import pygame as pg

from settings import *
from animation import *
from StartButton import StartButton
class Home:
  def __init__(self,game):
    self.game = game

    startButton = StartButton(450,250,103,28)

    while self.game.status == HOME:
      self.game.screen.blit(HOME_BG,(0,0))

      for event in pg.event.get():
        pos = pg.mouse.get_pos()

        if event.type == pg.QUIT:
          quit()

        if event.type == pg.MOUSEBUTTONDOWN:
          if startButton.hover(pos):
            self.game.status = START

        if event.type == pg.KEYDOWN:
          if event.key == pg.K_RETURN:
            self.game.status = START
        if event.type == pg.MOUSEMOTION:
          startButton.hover(pos)


      self.game.screen.blit(startButton.image,(450,250))
      pg.display.flip()