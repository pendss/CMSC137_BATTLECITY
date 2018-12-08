import pygame

from settings import *
from animation import *

class Waiting:
  def __init__(self,game):
    self.game = game

    counter = 0
    while self.game.status == WAITING:
      self.game.start()

      if counter == 100:
        self.game.screen.blit(WAIT0,(0,0))
      elif counter == 200:
        self.game.screen.blit(WAIT1,(0,0))
      elif counter == 300:
        self.game.screen.blit(WAIT2,(0,0))
      elif counter == 400:
        self.game.screen.blit(WAIT3,(0,0))
      elif counter == 500:
        self.game.screen.blit(WAIT4,(0,0))
      elif counter == 600:
        self.game.screen.blit(WAIT5,(0,0))
      elif counter == 700:
        self.game.screen.blit(WAIT6,(0,0))
      elif counter == 800:
        self.game.screen.blit(WAIT7,(0,0))
      elif counter == 900:
        self.game.screen.blit(WAIT8,(0,0))
        counter = 0
      counter += 1

      for event in pg.event.get():
        pos = pg.mouse.get_pos()

        if event.type == pg.QUIT:
          quit()

      pg.display.flip()