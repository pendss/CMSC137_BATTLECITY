import sys
import os
import socket
import select
import player_pb2
import tcp_packet_pb2
from threading import Thread
import tkinter
from tkinter import *
from tkinter import simpledialog

HOST = '202.92.144.45'
PORT = 80

#create socket and connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
sentm = ""

#create tcp packet
tcp = tcp_packet_pb2.TcpPacket()

def raise_frame(frame,choice):
	frame.tkraise()
	if choice==1:
		createLobby_Action()
	elif choice==2:
		connect_Action()


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

	maxplay = simpledialog.askinteger("Input","Max Players", parent=top)

	createLobby_packet.max_players = maxplay

	s.sendall(createLobby_packet.SerializeToString())
	data = s.recv(1024)
	createLobby_packet.ParseFromString(data)
	return createLobby_packet

def join_Lobby(lobby_id):
	lid = "Lobby ID: {}".format(lobby_id)
	lobbyLabel = Label(chatFrame, text=lid)
	lobbyLabel.pack()
	print(lid)

	connect_packet = Connect(player.name,player.id,lobby_id)
	connectedLabel = Label(chatFrame, text=connect_packet, fg="green")
	connectedLabel.pack()
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
					print(chat_packet.player.name + ": " + chat_packet.message)
					msg = chat_packet.player.name + ": " + chat_packet.message
					msg_list.insert(tkinter.END, msg)
				elif tcp.type == tcp.CONNECT:
					connect_packet.ParseFromString(data)
					print(player.name + " has joined the lobby")
					msg = player.name + " has joined the lobby"
					msg_list.insert(tkinter.END, msg)
				elif tcp.type == tcp.DISCONNECT:
					connect_packet.ParseFromString(data)
					print(player.name + " has disconnected from lobby")
					msg = player.name + " has disconnected from lobby"
					msg_list.insert(tkinter.END, msg)
				elif tcp.type == tcp.PLAYER_LIST:
					playerList_packet = tcp.PlayerListPacket()
					playerList_packet.ParseFromString(data)
					for players in playerList_packet.player_list:
						print("List of Players in the lobby")
						print(players.name)

			else:
				message = sys.stdin.readline().rstrip('\n')

				if message == "exit":
					disconnect_packet = tcp.DisconnectPacket()
					disconnect_packet.type = tcp.DISCONNECT
					s.sendall(disconnect_packet.SerializeToString())
					return
				elif message == "player-list":
					playerList_packet = tcp.PlayerListPacket()
					playerList_packet.type = tcp.PLAYER_LIST
					s.sendall(playerList_packet.SerializeToString())
				else:
					chat_packet.type = tcp.CHAT
					chat_packet.message = message
					chat_packet.player.name = player.name
					s.sendall(chat_packet.SerializeToString())

def createLobby_Action():
	createLobby_packet = create_Lobby()
	join_Lobby(createLobby_packet.lobby_id)

def connect_Action():
	lobby_id = simpledialog.askstring("Input", "Lobby ID", parent=top)
	join_Lobby(lobby_id)

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    sentm = my_msg.get()
    my_msg.set("")  # Clears input field.


top = tkinter.Tk()
top.title("Chat")
# top.geometry('1366x720')

menuFrame = Frame(top)
chatFrame = Frame(top)

for frame in (menuFrame, chatFrame):
	frame.grid(row=0,column=0,sticky='news')

name = simpledialog.askstring("Input", "Player Name", parent=top)

backButton = Button(chatFrame, text="Main Menu", command=lambda:raise_frame(menuFrame,0)).pack()

scrollbar = tkinter.Scrollbar(chatFrame)
msg_list = Listbox(chatFrame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
entry_field = tkinter.Entry(chatFrame, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(chatFrame, text="Send", command=send)
send_button.pack()


player = player_pb2.Player()
player.name = name

greeting = "Hi "+player.name+"!"

welcome = Label(menuFrame, text=greeting)
welcome.pack()

createLobbyButton = Button(menuFrame, text="Create Lobby", command=lambda:raise_frame(chatFrame,1))
createLobbyButton.pack(fill=X)

connectButton = Button(menuFrame, text="Connect", command=lambda:raise_frame(chatFrame,2))
connectButton.pack(fill=X)

exitButton = Button(menuFrame, text="Exit")
exitButton.pack(fill=X)

raise_frame(menuFrame,0)
top.mainloop()

while True:

	choice = Menu()

	if choice == 1:
		createLobby_packet = create_Lobby()
		join_Lobby(createLobby_packet.lobby_id)

	elif choice == 2:
		lobby_id = input("Lobby ID: ")
		join_Lobby(lobby_id)

	elif choice == 3:
		os.system('clear')
		break


s.close()