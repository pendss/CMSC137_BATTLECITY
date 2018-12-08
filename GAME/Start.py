import pygame

from settings import *
from animation import *

class Start:
  def __init__(self,game):
    self.game = game

    font = pg.font.Font('./PrStart.ttf', 35)

    while self.game.status == START:
      self.game.screen.blit(STARTNAME_BG,(0,0))
      text = font.render(self.game.name, True, BLACK)
      self.game.screen.blit(text, (250,230))

      for event in pg.event.get():

        if event.type == pg.QUIT:
          quit()

        if event.type == pg.KEYDOWN:
          if event.key == pg.K_RETURN:
            self.game.status = WAITING
            self.game.connect(self.game.name)
          elif event.key == pg.K_BACKSPACE:
            self.game.name = self.game.name[:-1]
          else:
            if len(self.game.name) < 16:
              self.game.name += event.unicode

      pg.display.flip()