import pygame
import os
from network import Network

clientNumber = 0
width = 800
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
spaceback = pygame.image.load('./assets/spaceback.png')
spaceback = pygame.transform.scale(spaceback,(width,height))

ship1 = pygame.image.load('./assets/ship1.png')
ship1 = pygame.transform.rotate(pygame.transform.scale(ship1,(100,100)), 270)
ship2 = pygame.image.load('./assets/ship2.png')
ship2 = pygame.transform.rotate(pygame.transform.scale(ship2,(100,100)), 90)

MAX_BULLET = 3
BULLET_COLOR = (255,0,0) #merah
BULLET_VEL = 5


class Player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self):
        return pygame.Rect(self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > 0 and self.x < width/2 or keys[pygame.K_LEFT] and self.x > width/2 + self.width/2:
            self.x -= self.vel

        if keys[pygame.K_RIGHT] and self.x < width - self.width and self.x > width/2 or keys[pygame.K_RIGHT] and self.x < width/2 - self.width/2:
            self.x += self.vel

        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel

        if keys[pygame.K_DOWN] and self.y < height - self.height:
            self.y += self.vel
            
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win,player, player2, bullet_counts):
    win.fill((100,100,100))

    #for background
    i = 0
    win.blit(spaceback, (i, 0))
    win.blit(spaceback, (width + i, 0))
    if (i == -width):
        win.blit(spaceback, (width + i, 0))
        i = 0
    i -= 1

    player.draw()
    win.blit(ship1, (player.x,player.y))

    player2.draw()
    win.blit(ship2, (player2.x, player2.y))

    for bullet in bullet_counts:
        pygame.draw.rect(win, BULLET_COLOR, bullet)
        
    pygame.display.update()

def bullet_handle(bullet_counts):
    for bullet in bullet_counts:
        bullet.x += BULLET_VEL
        
        if bullet.x > width:
            bullet_counts.remove(bullet)

def main():
    PLAYER_HEIGHT = 100
    PLAYER_WIDTH = 100
    bullet_counts = []
    rotate = 0
    
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0],startPos[1],PLAYER_HEIGHT,PLAYER_WIDTH)
    p2 = Player(0,0,PLAYER_HEIGHT, PLAYER_WIDTH)
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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bullet_counts) < MAX_BULLET:
                    bullet = pygame.Rect(p.x + p.width, p.y + int(p.height/2), 10, 5)
                    bullet_counts.append(bullet)
        
        redrawWindow(win, p, p2, bullet_counts) 
        p.move()
        bullet_handle(bullet_counts)
                    
if __name__ == "__main__":
    main()