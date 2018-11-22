'''
CMSC 137 Tankehin Mo To (Battle City)
@authors
  Afable, Lorenz Matthew
  Cuenca, Paulo Anton
  Tolentino, Caroline
@section
  AB-5L
@Description
  An implementation of a TCP client that connects to a TCP server with IP address 202.92.144.45 and port 80
'''

import socket, os, sys, errno, select
import player_pb2, tcp_packet_pb2

# create TCP packet
tcpPacket = tcp_packet_pb2.TcpPacket()
# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ask user for valid option
def getOption():
  print("Options:\n 1. Create Lobby\n 2. Join Lobby\n 3. Exit\n")

  option = 0
  while option not in [1,2,3]: # make user input a valid option
    try:
      option = int(input("Choose option: "))
    except ValueError:
      print("That is not an option.")

  return option

def createPlayer(player):
  player.name = input("Player name: ")

def createLobby():
  os.system('clear')
  print("Create Lobby")
  packet = tcpPacket.CreateLobbyPacket()
  packet.type = tcpPacket.CREATE_LOBBY
  packet.max_players = 0
  while packet.max_players < 3 or packet.max_players > 16: # ask user for maximum number of players
    try:
      packet.max_players = int(input("Enter maximum number of players (3-16): "))

      if packet.max_players < 3 or packet.max_players > 16:
        print("Please enter a number from 3-16.")
    except ValueError:
      print("Invalid input")

  s.sendall(packet.SerializeToString())
  data = s.recv(1024)
  packet.ParseFromString(data)
  return packet

def joinLobby(lobby_id):
  '''
    @TODO: Handle lobby errors (ErrLdnePacket, ErrLfullPacket, ErrPacket)
  '''
  print("Welcome to Lobby {}".format(lobby_id))
  packet = tcpPacket.ConnectPacket()
  packet.type = tcpPacket.CONNECT
  packet.player.name = player.name
  packet.lobby_id = lobby_id

  s.sendall(packet.SerializeToString()) # send a join lobby request
  data = s.recv(1024)
  tcpPacket.ParseFromString(data)

  while True:
    socket_list = [sys.stdin, s]
    read_sockets, write_sockets, error_socket = select.select(socket_list, [], [])
    
    chatPacket = tcpPacket.ChatPacket()
    for sockets in read_sockets:
      if sockets == s:
        data = s.recv(1024)
        tcpPacket.ParseFromString(data)
        if tcpPacket.type == tcpPacket.CHAT:
          chatPacket.ParseFromString(data)
          print("{}: {}".format(chatPacket.player.name, chatPacket.message))
        elif tcpPacket.type == tcpPacket.CONNECT:
          packet.ParseFromString(data)
          print("{} has joined the lobby.".format(packet.player.name))
        elif tcpPacket.type == tcpPacket.DISCONNECT:
          packet.ParseFromString(data)
          print("{} has disconnected from the lobby.".format(packet.player.name))
        elif tcpPacket.type == tcpPacket.PLAYER_LIST:
          playerListPacket = tcpPacket.PlayerListPacket()
          playerListPacket.ParseFromString(data)
          count = 1
          for player_in_list in playerListPacket.player_list:
            print("{}. {}".format(count, player_in_list.name))
            count += 1

      else:
        message = sys.stdin.readline().rstrip('\n')
        if message == "exit":
          disconnectPacket = tcpPacket.DisconnectPacket()
          disconnectPacket.type = tcpPacket.DISCONNECT
          s.sendall(disconnectPacket.SerializeToString())
          return
        elif message == "list_players":
          playerListPacket = tcpPacket.PlayerListPacket()
          playerListPacket.type = tcpPacket.PLAYER_LIST
          s.sendall(playerListPacket.SerializeToString())
        else:
          chatPacket.message = message
          chatPacket.type = tcpPacket.CHAT
          chatPacket.player.name = player.name
          s.sendall(chatPacket.SerializeToString())

def Main(host, port):
  try: # handle socket errors
    s.connect((host, port))
    while True:
      option = getOption()

      if option == 1: # create lobby
        lobby_id = createLobby().lobby_id
        joinLobby(lobby_id)

      elif option == 2:
        lobby_id = input("Enter lobby ID: ")
        joinLobby(lobby_id)

      elif option == 3:
        os.system('clear')
        break

    s.close()
  except socket.error as error:
    if error.errno == errno.ENETUNREACH:
      print("\n***Network unreachable***\n")
    elif error.errno == errno.ECONNREFUSED:
      print("\n***Connection refused***\n")
    else:
      raise

# create player
player = player_pb2.Player()
createPlayer(player)
if __name__ == '__main__':
  Main("202.92.144.45", 80)