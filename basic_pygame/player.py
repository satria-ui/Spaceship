import pygame

width = 800
height = 800

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
