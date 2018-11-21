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
	connect_packet.ParseFromString(data)
	return connect_packet

player = player_pb2.Player()
player.name = input("Player name: ")	

while True:
	
	choice = Menu()

	if choice == 1:
			
		createLobby_packet = tcp.CreateLobbyPacket()
		createLobby_packet.type = tcp.CREATE_LOBBY
		createLobby_packet.max_players = 4
		s.sendall(createLobby_packet.SerializeToString())
		data = s.recv(1024)
		createLobby_packet.ParseFromString(data)

		connect_packet = Connect(player.name,player.id,createLobby_packet.lobby_id)
		print(connect_packet)
		while True:
			message = input("message: ")
			if message == "exit": break

	elif choice == 2:
		lobby_id = input("Lobby ID: ")
		connect_packet = Connect(player.name,player.id,lobby_id)
		while True:
			read_sockets,write_sockets,error_sockets = select.select([s],[],[])
			message = input("message: ")
			if message == "exit": break
	elif choice == 3:
		os.system('clear')
		break			
s.close()