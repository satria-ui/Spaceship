import socket
from _thread import *
from player import Player
import pickle

server = "192.168.56.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

PLAYER_HEIGHT = 100
PLAYER_WIDTH = 100

players = [Player(100,400,PLAYER_WIDTH,PLAYER_HEIGHT, (255,0,0), 270), Player(700,400,PLAYER_WIDTH,PLAYER_HEIGHT, (0,255,0), 90)]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 0:
                    reply = players[1]
                elif player == 1:
                    reply = players[0]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


#save number of player
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    #counter to keep track current player
    currentPlayer += 1