import sys
import pygame as pg
import random
import socket
from threading import Thread
from Chat import Chat
if len(sys.argv) == 1:
    print('python/python3 game.py [ip_address]')
    quit()

from Home import Home
from Start import Start
from Waiting import Waiting
from settings import *
from sprites import *
from animation import *

import json

HOST = sys.argv[1]
PORT = 10000
BUFFER = 1024
ADDRESS = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.status = HOME
        self.running = True
        self.name = ''
        self.chat_enter = False
        self.chat_init = False
        self.chat = ''
        self.chatMessages = []
        self.game_t = Thread(target=self.receive)
        self.game_t.daemon = True
        self.game_t.start()

        self.chat_bg = CHAT_BG.convert()
        self.chat1_bg = CHAT1_BG.convert()

        self.players = {}

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.bricks = pg.sprite.Group()
        self.all_players = pg.sprite.Group()
        self.run()

    def run(self):
        # Game Loop
        while True:

          if self.status == HOME:
            Home(self)

          elif self.status == START:
            Start(self)

          elif self.status == WAITING:
            Waiting(self)

          elif self.status == GAME:

            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

    def events(self):
        # Game Loop -

        for event in pg.event.get():
            # check for closing window
          if event.type == pg.QUIT:
            self.chat_lobby.lobby_disconnect(self.name) 
            quit()

          if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
              if self.chat_enter == True:
                if len(self.chatMessages) > 12:
                  self.chatMessages.pop(0)
                # self.game.status = WAITING
                # self.game.connect(self.game.name)

                # self.chatMessages.append(self.name+": "+self.chat)
                self.chat_lobby.lobby_chat(self.name,": "+self.chat)
                # print(self.chat_lobby)
                self.chat_enter = False
                # print(self.chatMessages)
                self.chat = ''

              elif self.chat_enter == False:
                self.chat_enter = True
            elif event.key == pg.K_BACKSPACE:
              self.chat = self.chat[:-1]
            else:
              if len(self.chat) < 16 and self.chat_enter == True:
                self.chat += event.unicode


    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        if self.chat_enter == False:
          self.screen.blit(self.chat1_bg,(700,0))
        else: self.screen.blit(self.chat_bg,(700,0))
        self.all_sprites.draw(self.screen)

        font = pg.font.Font('./PrStart.ttf', 15)
        text = font.render(self.chat, True, WHITE)
        self.screen.blit(text, (750,455))

        font2 = pg.font.Font('./PrStart.ttf', 8)

        for i in range(0,len(self.chatMessages)):
          text2 = font2.render(self.chatMessages[i], True, WHITE)
          self.screen.blit(text2, (730,95+(i*25)))
        # *after* drawing everything, flip the display
        pg.display.flip()

    def receive(self):
      while self.running:
        data, address = s.recvfrom(BUFFER)

        if data:
          msg = data.decode().split()
          request = msg[0]
          if request == 'start':
            self.status = GAME
            msg.pop(0)
            msg = ' '.join(msg)
            msg = msg.split('|')
            data = json.loads(msg[0])
            players = json.loads(msg[1])
            lobby_id = msg[2]

            for i in range(0, len(data)):
              for j in range(0, len(data[i])):
                if data[i][j] == 1:
                  brick = Brick([j*50,i*50])
                  self.all_sprites.add(brick)
                  self.bricks.add(brick)

            # for name, values in players.items():
            #   x = float(values['x'])
            #   y = float(values['y'])
            #   health = int(values['health'])
            #   move = values['move']
            #   player = Player(self, name, [x,y], move, health)
            #   self.players[name] = player
            #   self.all_sprites.add(player)
            if not self.chat_init:
              self.chat_lobby = Chat(self)
              self.chat_lobby.Connect(self.name, lobby_id)
              self.chat_t = Thread(target=self.chat_lobby.lobby_joined)
              self.chat_t.daemon = True
              self.chat_t.start()

    def send(self, msg):
      s.sendto(str.encode(msg), ADDRESS)

    def connect(self, name):
      msg = 'connect '
      msg += name
      self.send(msg)

    def start(self):
      msg = 'start'
      self.send(msg)

g = Game()
while g.running:
    g.new()

pg.quit()