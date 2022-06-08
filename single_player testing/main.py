import pygame
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")

BACKGROUNDCOLOR = (100,100,100)
BORDER_COLOR = (0,0,0)
BULLET_COLOR = (255,0,0)
BORDER = pygame.Rect(int(WIDTH/2) - 5, 0, 10, HEIGHT)
BACKGROUND = pygame.transform.scale(pygame.image.load('./img/background.png'), (WIDTH, HEIGHT))

FPS = 60
VEL = 3
BULLET_VEL = 20
MAX_BULLET = 3

YELLOW_HIT = pygame.USEREVENT + 1
BLACK_HIT = pygame.USEREVENT + 2 

HIT_SOUND = pygame.mixer.Sound("./sounds/hit.mp3")
SHOOT_SOUND = pygame.mixer.Sound("./sounds/gun_sound.mp3")

HEALTH_FONT = pygame.font.SysFont('freesansbold.ttf', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 80)

SPACESHIP_WIDTH, SPACESHIP_HEIGT = 55,40
YELLOW_SPACESHIP_IMG = pygame.image.load('./img/yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_HEIGT,SPACESHIP_WIDTH)), 270)
BLACK_SPACESHIP_IMG = pygame.image.load('./img/black.png')
BLACK_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLACK_SPACESHIP_IMG, (SPACESHIP_HEIGT,SPACESHIP_WIDTH)), 90)

def draw_window(black, yellow, black_bullets, yellow_bullets, black_health, yellow_health):
    WIN.blit(BACKGROUND, (0,0))
    # WIN.fill(BACKGROUNDCOLOR)
    pygame.draw.rect(WIN, BORDER_COLOR, BORDER)
    black_health_text = HEALTH_FONT.render("Health: " +str(black_health), True, BULLET_COLOR)
    yellow_health_text = HEALTH_FONT.render("Health: " +str(yellow_health), True, BULLET_COLOR)
    WIN.blit(black_health_text, (WIDTH - black_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(BLACK_SPACESHIP, (black.x, black.y))
    
    for bullet in black_bullets:
        pygame.draw.rect(WIN, BULLET_COLOR, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, BULLET_COLOR, bullet)
    
    pygame.display.update()

def yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x-VEL > 0:
        yellow.x -= VEL
    if key_pressed[pygame.K_s] and yellow.y+VEL+yellow.height < HEIGHT+13:
        yellow.y += VEL
    if key_pressed[pygame.K_w] and yellow.y-VEL > 0:
        yellow.y -= VEL
    if key_pressed[pygame.K_d] and yellow.x+VEL+yellow.width < BORDER.x - 14:
        yellow.x += VEL

def black_movement(key_pressed, black):
    if key_pressed[pygame.K_LEFT] and black.x-VEL > BORDER.x + 12:
        black.x -= VEL
    if key_pressed[pygame.K_DOWN] and black.y+VEL+black.height < HEIGHT+13:
        black.y += VEL
    if key_pressed[pygame.K_UP] and black.y-VEL > 0:
        black.y -= VEL
    if key_pressed[pygame.K_RIGHT] and black.x+VEL+black.width < WIDTH-10:
        black.x += VEL

def bullet_handle(black_bullets, yellow_bullets, yellow, black):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
        elif black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLACK_HIT))
            yellow_bullets.remove(bullet)
    
    for bullet in black_bullets:
        bullet.x -= BULLET_VEL
        if bullet.x < 0:
            black_bullets.remove(bullet)
        elif yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            black_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, (255,255,255))
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    
def main():
    yellow = pygame.Rect(50,400, SPACESHIP_HEIGT, SPACESHIP_WIDTH)
    black = pygame.Rect(700,400, SPACESHIP_HEIGT, SPACESHIP_WIDTH)
    
    yellow_bullets = []
    black_bullets = []
    yellow_health = 10
    black_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        draw_window(black,yellow, black_bullets, yellow_bullets, black_health, yellow_health)
        
        key_pressed = pygame.key.get_pressed()
        yellow_movement(key_pressed, yellow)
        black_movement(key_pressed, black)
        bullet_handle(black_bullets, yellow_bullets, yellow, black)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x+yellow.width, yellow.y+int(yellow.height/2), 10, 5)
                    yellow_bullets.append(bullet)
                    SHOOT_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(black_bullets) < MAX_BULLET:    
                    bullet = pygame.Rect(black.x, black.y+int(black.height/2), 10, 5)
                    black_bullets.append(bullet)
                    SHOOT_SOUND.play()
                    
            if event.type == BLACK_HIT:
                black_health -= 1
                HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                HIT_SOUND.play()
                
        winner_text = ""
        if black_health <= 0:
            winner_text = "Yellow Wins"
        if yellow_health <= 0:
            winner_text = "Black Wins"
        
        if winner_text != "":
            draw_winner(winner_text)
            break
        
    main()

if __name__ == "__main__":
    main()