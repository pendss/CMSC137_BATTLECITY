import pygame as pg


class StartButton:
  def __init__(self,x,y,width,height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.image = pg.image.load("./sprites/start.png")

  def hover(self,mouse_pos):
    if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width:
      if mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
        self.image = pg.image.load("./sprites/start1.png")
        return True

    self.image = pg.image.load("./sprites/start.png")
    return False