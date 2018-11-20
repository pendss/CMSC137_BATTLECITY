import sys
import socket
import player_pb2
import tcp_packet_pb2


HOST = '202.92.144.45'
PORT = 80


client = player_pb2.Player() # create object of player
client.name = "ganoyaaa"
client.id = "2"

connect_packet = tcp_packet_pb2.TcpPacket.ConnectPacket()
connect_packet.type = tcp_packet_pb2.TcpPacket.CONNECT
connect_packet.player.name = client.name
connect_packet.player.id = client.id
connect_packet.lobby_id = "TROUU"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST,PORT))
	s.sendall(connect_packet.SerializeToString())
	data2 = s.recv(1024)
print("received: " + str(connect_packet.ParseFromString(data2)))
print(connect_packet)