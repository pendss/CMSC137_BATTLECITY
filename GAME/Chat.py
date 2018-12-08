import sys
import os
import socket
import select
import player_pb2
import tcp_packet_pb2
from threading import Thread

HOST = '202.92.144.45'
PORT = 80

#create socket and connect to server
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST,PORT))

#create tcp packet
tcp = tcp_packet_pb2.TcpPacket()

class Chat:
  def __init__(self,game='none'):
    self.game = game
    self.tcp = tcp
    # self.game.chat_init = False
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect((HOST,PORT))

  def Connect(self,name,lobby_id):
    connect_packet = self.tcp.ConnectPacket()
    connect_packet.type = self.tcp.CONNECT
    connect_packet.player.name = name
    connect_packet.lobby_id = lobby_id
    self.game.chat_init = True
    self.send_receive(connect_packet)

    # Thread(target=self.lobby_joined).start()

  def lobby_joined(self):
    while self.game.running:
      chat_packet = self.tcp.ChatPacket()
      data = self.s.recv(1024)
      self.tcp.ParseFromString(data)
      print(tcp)
      # print(chat_packet.ParseFromString(data))
      if self.tcp.type == self.tcp.CHAT:
        chat_packet.ParseFromString(data)
        if len(self.game.chatMessages) > 12:
          self.game.chatMessages.pop(0)
        self.game.chatMessages.append(chat_packet.player.name+": "+chat_packet.message)
      elif self.tcp.type == self.tcp.CONNECT:
        connect_packet = self.tcp.ConnectPacket()
        connect_packet.ParseFromString(data)
        print(connect_packet)
        if len(self.game.chatMessages) > 12:
          self.game.chatMessages.pop(0)
        self.game.chatMessages.append(connect_packet.player.name+" has connected!")
      elif self.tcp.type == self.tcp.DISCONNECT:
        disconnect_packet = self.tcp.DisconnectPacket()
        disconnect_packet.ParseFromString(data)
        if len(self.game.chatMessages) > 12:
          self.game.chatMessages.pop(0)
        self.game.chatMessages.append(disconnect_packet.player.name+" has disconnected!")

  def lobby_disconnect(self,name):
      disconnect_packet = self.tcp.DisconnectPacket()
      disconnect_packet.type = self.tcp.DISCONNECT
      disconnect_packet.player.name = name
      self.send_receive(disconnect_packet)

  def lobby_chat(self,name,message):
    chat_packet = self.tcp.ChatPacket()
    chat_packet.type = self.tcp.CHAT
    chat_packet.message = message
    chat_packet.player.name = name
    print(chat_packet)
    self.s.sendall(chat_packet.SerializeToString())

  def lobby_players(self):
    players_packet = self.tcp.PlayerListPacket()
    players_packet.type = self.tcp.PLAYER_LIST

    players_packet = self.send_receive(players_packet)

    return players_packet

  def send_receive(self,tcp_packet):
    self.s.sendall(tcp_packet.SerializeToString())
    data = self.s.recv(1024)
    tcp_packet.ParseFromString(data)
    return tcp_packet

  def create_Lobby(self,max_players):
    createLobby_packet = self.tcp.CreateLobbyPacket()
    createLobby_packet.type = self.tcp.CREATE_LOBBY
    createLobby_packet.max_players = max_players

    createLobby_packet = self.send_receive(createLobby_packet)
    return createLobby_packet



# while True:

# 	choice = Menu()

# 	if choice == 1:
# 		os.system('clear')
# 		createLobby_packet = create_Lobby()
# 		join_Lobby(createLobby_packet.lobby_id)

# 	elif choice == 2:
# 		os.system('clear')
# 		lobby_id = input("Lobby ID: ")
# 		join_Lobby(lobby_id)

# 	elif choice == 3:
# 		os.system('clear')
# 		break
# s.close()