import pygame
pygame.font.init()

width = 800
height = 800
BULLET_COLOR = (255,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
HEALTH_FONT = pygame.font.SysFont('freesansbold.ttf', 40)

class Player():
    def __init__(self, x, y, width, height, color, rotation, bullet_pos):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        self.rotation = rotation
        self.bullet_pos = bullet_pos
        self.player = pygame.Rect(self.rect)

    def draw(self, win, ship, bullet_counts, bullet_enemy_counts, enemy_health, player_health):
        enemy_health_text = HEALTH_FONT.render("Enemy Health: " + str(enemy_health), True, RED)
        player_health_text = HEALTH_FONT.render("Player Health: " + str(player_health), True, GREEN)
        win.blit(enemy_health_text, (width - enemy_health_text.get_width() - 10, 10))
        win.blit(player_health_text, (10, 10))
    
        # pygame.draw.rect(win, self.color, self.rect)
        win.blit(ship, (self.rect[0],self.rect[1]))
        
        
        for bullet in bullet_counts:
            pygame.draw.rect(win, BULLET_COLOR, bullet)
            
        for bullet2 in bullet_enemy_counts:
            pygame.draw.rect(win, BULLET_COLOR, bullet2)

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
