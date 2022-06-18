import socket
from _thread import *
from player import Player
import pygame
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
PLAYER1_X = 100
PLAYER1_Y = 400
PLAYER2_X = 700
PLAYER2_Y = 400

bullet_counts = []
bullet_right = []
bullet_left = []
BULLET_VEL = 5
MAX_BULLET = 3
width = 800
height = 800
BULLET_COLOR = (255,0,0)

bullet = pygame.Rect(PLAYER_WIDTH/2, PLAYER1_Y + int(PLAYER_HEIGHT/2), 10, 5)
# bullet_right = bullet.x + BULLET_VEL
# bullet_left = bullet.x - BULLET_VEL


players = [Player(PLAYER1_X,PLAYER1_Y,PLAYER_WIDTH,PLAYER_HEIGHT, (255,0,0), 270, bullet_right), Player(PLAYER2_X,PLAYER2_Y,PLAYER_WIDTH,PLAYER_HEIGHT, (0,255,0), 90, bullet_left)]


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
    
    