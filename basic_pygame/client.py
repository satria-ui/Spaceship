import pygame
import os
from network import Network

clientNumber = 0
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
spaceback = pygame.image.load('assets\spaceback.png')
spaceback = pygame.transform.scale(spaceback,(width,height))
ship1 = pygame.image.load('assets\ship1.png')
ship1 = pygame.transform.scale(ship1,(width*0.2,height*0.2))
ship2 = pygame.image.load('assets\ship2.png')
ship2 = pygame.transform.scale(ship2,(width*0.2,height*0.2))


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        # self.image = pygame.image.load(os.path.join('resources', 'assets/ship1.png'
        # self.rect = self.image.get_rect(topleft=pos)
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win,player, player2):
    win.fill((255,255,255))

    #for background
    i = 0
    win.blit(spaceback, (i, 0))
    win.blit(spaceback, (width + i, 0))
    if (i == -width):
        win.blit(spaceback, (width + i, 0))
        i = 0
    i -= 1

    player.draw(win)
    win.blit(ship1, (player.x,player.y))

    player2.draw(win)
    win.blit(ship2, (player2.x, player2.y))

    pygame.display.update()


def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0],startPos[1],100,100,(0,255,0))
    p2 = Player(0,0,100,100,(255,0,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2)

main()