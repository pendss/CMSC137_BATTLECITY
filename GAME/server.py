import socket
import json
from Chat import Chat

HOST = '0.0.0.0'
PORT = 10000
BUFFER = 1024
ADDRESS = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(ADDRESS)

player_count = 0
players = {}
arena = []

created_chat = False
chat_lobby = ''

while True:
    data, address = s.recvfrom(BUFFER)

    string = data.decode().split()
    request = string[0]

    if request == 'connect':
        print('{} connected'.format(string[1]))
        player_count += 1

        if player_count == 1:
            x = '50'
            y = '50'
            move = 'down'
        elif player_count == 2:
            x = '600'
            y = '50'
            move ='left'
        elif player_count == 3:
            x = '50'
            y = '400'
            move = 'right'
        elif player_count == 4:
            x = '600'
            y = '400'
            move = 'up'

        players[string[1]] = {
            'health': '100',
            'x': x,
            'y': y,
            'move': move
        }

    elif request == 'start':
        data = 'none'
        data = str.encode(data)
        if len(players) == 2:
            if not created_chat:
                created_chat = True
                chat = Chat()
                chat_lobby = chat.create_Lobby(4)
                chat_lobby = chat_lobby.lobby_id
                print("Created chat lobby {}".format(chat_lobby))

            # 0 - empty | 1 - brick | 2 - grass | 3 - player
            arena = [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,3,1,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,1,0,0,0,0,0,0,0,0,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,0,0,0,0,0,0,0,0,1,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,1,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ]
            data = 'start '
            data += json.dumps(arena) + '|' + json.dumps(players) + '|' + chat_lobby
            data = str.encode(data)


    if data:
        s.sendto(data, address)
