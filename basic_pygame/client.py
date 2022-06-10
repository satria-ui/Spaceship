import pygame
import os
from network import Network
from player import Player

width = 800
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spaceship")
# spaceback = pygame.image.load('./assets/spaceback.png')
# spaceback = pygame.transform.scale(spaceback,(width,height))

MAX_BULLET = 3
BULLET_COLOR = (255,0,0) #merah
BULLET_VEL = 5


def draw_window(win,player, player2, bullet_counts):
    win.fill((100,100,100))
    #for background
    # i = 0
    # win.blit(spaceback, (i, 0))
    # win.blit(spaceback, (width + i, 0))
    # if (i == -width):
    #     win.blit(spaceback, (width + i, 0))
    #     i = 0
    # i -= 1
    
    # ship1 = pygame.image.load('./assets/ship1.png')
    # ship1 = pygame.transform.rotate(pygame.transform.scale(ship1,(100,100)), 270)
    # ship2 = pygame.image.load('./assets/ship2.png')
    # ship2 = pygame.transform.rotate(pygame.transform.scale(ship2,(100,100)), 90)
    
    # win.blit(ship1, (player.x,player.y))
    player.draw(win)

    # win.blit(ship2, (player2.x, player2.y))
    player2.draw(win)
    
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
    p = n.getP()
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        p2 = n.send(p)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bullet_counts) < MAX_BULLET:
                    bullet = pygame.Rect(p.x + p.width, p.y + int(p.height/2), 10, 5)
                    bullet_counts.append(bullet)
        
        draw_window(win, p, p2, bullet_counts) 
        p.move()
        bullet_handle(bullet_counts)
                    
if __name__ == "__main__":
    main()