import pygame
import os
from network import Network
from player import Player
pygame.mixer.init()
pygame.font.init()

width = 800
height = 800
ENEMY_HIT = pygame.USEREVENT + 1
PLAYER_HIT = pygame.USEREVENT + 2
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("CLIENT 1")
spaceback = pygame.image.load('./assets/spaceback.png')
spaceback = pygame.transform.scale(spaceback,(width,height))
HIT_SOUND = pygame.mixer.Sound("./assets/hit.mp3")
SHOOT_SOUND = pygame.mixer.Sound("./assets/gun_sound.mp3")

WINNER_FONT = pygame.font.SysFont('comicsans', 80)
MAX_BULLET = 3
# BULLET_COLOR = (255,0,0) #merah
BULLET_VEL = 5


def draw_window(win,player, enemy, bullet_counts, bullet_enemy_counts, enemy_health, player_health):
    win.fill((100,100,100))
    # for background
    i = 0
    win.blit(spaceback, (i, 0))
    win.blit(spaceback, (width + i, 0))
    if (i == -width):
        win.blit(spaceback, (width + i, 0))
        i = 0
    i -= 1
    
    ship = pygame.image.load('./assets/ship1.png')
    ship = pygame.transform.rotate(pygame.transform.scale(ship,(100,100)), player.rotation)
    ship2 = pygame.image.load('./assets/ship2.png')
    ship2 = pygame.transform.rotate(pygame.transform.scale(ship2,(100,100)), enemy.rotation)
    
    # win.blit(ship1, (player.x,player.y))
    player.draw(win, ship, bullet_counts, bullet_enemy_counts, enemy_health, player_health)
    print("PLAYER: " + str(player_health))

    # win.blit(ship2, (player2.x, player2.y))
    enemy.draw(win, ship2, bullet_counts, bullet_enemy_counts, enemy_health, player_health)
    print("ENEMY: " + str(enemy_health))
    
    # for bullet in bullet_counts:
    #     pygame.draw.rect(win, BULLET_COLOR, bullet)
        
    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, (255,255,255))
    win.blit(draw_text, (width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def bullet_handle(bullet_counts, p2):
    for bullet in bullet_counts:
        bullet.x += BULLET_VEL
        if bullet.x > width:
            bullet_counts.remove(bullet)
        elif pygame.Rect.colliderect(bullet,p2.player):
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            bullet_counts.remove(bullet)
        # elif p.player.colliderect(bullet):
            # pygame.event.post(pygame.event.Event(PLAYER_HIT))
            # bullet_counts.remove(bullet)

def bullet_enemy_handle(bullet_enemy_counts, p):
    for bullet in bullet_enemy_counts:
        bullet.x -= BULLET_VEL
        if bullet.x < 0:
            bullet_enemy_counts.remove(bullet)
        elif pygame.Rect.colliderect(bullet,p.player):
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
            bullet_enemy_counts.remove(bullet)
        # elif p.player.colliderect(bullet):
            # pygame.event.post(pygame.event.Event(PLAYER_HIT))
            # bullet_counts.remove(bullet)


def main():
    PLAYER_HEIGHT = 100
    PLAYER_WIDTH = 100
    bullet_counts = []
    bullet_enemy_counts = []
    enemy_health = 10
    player_health  = 10
    
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
                        bullet = pygame.Rect(p.x + int(p.width/2), p.y + int(p.height/2), 10, 5)
                        p.bullet_pos.append(bullet)
                        SHOOT_SOUND.play()
                        
            if event.type == ENEMY_HIT:
                enemy_health -= 1
                HIT_SOUND.play()
            if event.type == PLAYER_HIT:
                player_health -= 1
                HIT_SOUND.play()
        
        draw_window(win, p, p2, p.bullet_pos, p2.bullet_pos, enemy_health, player_health)
        p.move()
        bullet_handle(p.bullet_pos,p2)
        bullet_enemy_handle(p2.bullet_pos,p)
        
        winner_text = ""
        if player_health <= 0:
            winner_text = "You Lose"
        if enemy_health <= 0:
            winner_text = "You Win"
        if winner_text != "":
            draw_winner(winner_text)
            break
                    
if __name__ == "__main__":
    main()