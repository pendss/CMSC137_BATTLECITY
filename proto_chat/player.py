import sys
import socket
import player_pb2
import tcp_packet_pb2
from threading import Thread

HOST = '202.92.144.45'
PORT = 80


def Menu():
	print("[1] - Create Lobby")
	print("[2] - Connect")
	print("[3] - Disconnect")
	x = input("choice: ")
	return x

choice = Menu()
if choice == "1":

	host = player_pb2.Player() # create object of player
	host.name = "ganoya"
	host.id = "1"

	createLobby = tcp_packet_pb2.TcpPacket.CreateLobbyPacket() # create object create lobby
	createLobby.type = tcp_packet_pb2.TcpPacket.CREATE_LOBBY
	createLobby.max_players = 4
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST,PORT))
		s.sendall(createLobby.SerializeToString())
		data = s.recv(1024)
	createLobby.ParseFromString(data)
	print(createLobby)
elif choice == "2":

	client = player_pb2.Player() # create object of player
	client.name = "ganoyaaa"
	client.id = "2"
	connect_packet = tcp_packet_pb2.TcpPacket.ConnectPacket()
	connect_packet.type = tcp_packet_pb2.TcpPacket.CONNECT
	connect_packet.player.name = client.name
	connect_packet.player.id = client.id
	connect_packet.lobby_id = "GQVUE"

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST,PORT))
		s.sendall(connect_packet.SerializeToString())
		data = s.recv(1024)

	connect_packet.ParseFromString(data)
	print(connect_packet)





# print("received: " + str(createLobby.ParseFromString(data1)))
# print("ID: " + createLobby.lobby_id)
# print(createLobby)

# #--------------


# print("received: " + str(connect_packet.ParseFromString(data2)))
# print(connect_packet)