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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#create tcp packet
tcp = tcp_packet_pb2.TcpPacket()



def Menu():
	print("[1] - Create Lobby")
	print("[2] - Connect")
	print("[3] - Exit")
	x = input("choice: ")
	return int(x)


def Connect(name,player_id,lobby_id):
	connect_packet = tcp.ConnectPacket()
	connect_packet.type = tcp.CONNECT
	connect_packet.player.name = name
	connect_packet.player.id = player_id
	connect_packet.lobby_id = lobby_id
	s.sendall(connect_packet.SerializeToString())
	data = s.recv(1024)
	tcp.ParseFromString(data)
	return tcp

def create_Lobby():
	createLobby_packet = tcp.CreateLobbyPacket()
	createLobby_packet.type = tcp.CREATE_LOBBY
	createLobby_packet.max_players = int(input("Max Players: "))

	s.sendall(createLobby_packet.SerializeToString())
	data = s.recv(1024)
	createLobby_packet.ParseFromString(data)
	return createLobby_packet

player = player_pb2.Player()
player.name = input("Player name: ")

def join_Lobby(lobby_id):
	print("Lobby ID: {}".format(lobby_id))
	connect_packet = Connect(player.name,player.id,lobby_id)
	print(connect_packet)
	# os.system("stty -echo")
	while True:
		sockets = [sys.stdin,s]
		read_sockets,write_sockets,error_sockets = select.select(sockets,[],[])

		chat_packet = tcp.ChatPacket()
		for socket in read_sockets:
			if socket == s:
				data = s.recv(1024)
				tcp.ParseFromString(data)

				if tcp.type == tcp.CHAT:
					chat_packet.ParseFromString(data)
					#print("{}: {}".format(chat_packet.player.name,chat_packet.message))
					print(chat_packet.player.name + ": " + chat_packet.message)
			else:
				message = sys.stdin.readline().rstrip('\n')
				chat_packet.type = tcp.CHAT
				chat_packet.message = message
				chat_packet.player.name = player.name
				s.sendall(chat_packet.SerializeToString())
				# os.system("stty -echo")
				# sys.stdout.write(player.name + ": ")
				# sys.stdout.write(message)
				# sys.stdout.flush()


while True:

	choice = Menu()

	if choice == 1:

		# createLobby_packet = tcp.CreateLobbyPacket()
		# createLobby_packet.type = tcp.CREATE_LOBBY
		# createLobby_packet.max_players = 4
		# s.sendall(createLobby_packet.SerializeToString())
		# data = s.recv(1024)
		# createLobby_packet.ParseFromString(data)
		createLobby_packet = create_Lobby()
		#connect_packet = Connect(player.name,player.id,createLobby_packet.lobby_id)
		join_Lobby(createLobby_packet.lobby_id)

	elif choice == 2:
		lobby_id = input("Lobby ID: ")
		join_Lobby(lobby_id)

	elif choice == 3:
		os.system('clear')
		break
s.close()