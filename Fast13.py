# --------------- IMPORTS -----------------
import pygame, sys
from pygame.locals import *
import random, time

# Initialize pygame modules
pygame.init()


# ---------------------------------------
# -------------- VARIABLES --------------

FPS = pygame.time.Clock()

# -------- Colors --------
BLACK = pygame.Color('black')           # Black
BLUE = pygame.Color('dodgerblue4')      # Blue
GREEN = pygame.Color('darkolivegreen')  # Green
GREY = pygame.Color('grey')             # Grey
RED = pygame.Color('indianred4')        # Red
WHITE = pygame.Color('white')           # White

# ---- Other Variables ----
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

# -------- Fonts --------
font = pygame.font.SysFont('Verdana', 60)
font_small = pygame.font.SysFont('Verdana', 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load('./image/AnimatedStreet.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT * 2))
i = 0

pygame.mixer.music.load('./audio/background.wav')
pygame.mixer.music.play(-1)

# ----- White Screen ------
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Fast 13")


# --------------------------------------
# -------------- CLASSES ---------------

# -------- Enemy --------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./image/Enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)


# -------- Player --------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load('./image/Player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 350:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -10)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 10)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-10, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(10, 0)


# ------- Sprites -------
P1 = Player()
E1 = Enemy()

# ------ Sprite Groups ------
enemies = pygame.sprite.Group()
enemies.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# ------- User Events -------
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


# ----------------------------------------
# ----------- GAME LOOP BEGINS -----------
while True:

    # ---- Loop Through Event List ----
    for event in pygame.event.get():

        # Increase Enemy Speed
        if event.type == INC_SPEED:
            SPEED += 0.5

        # Quit Game Loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(background, (0, i))
    DISPLAYSURF.blit(background, (0, -SCREEN_HEIGHT + i))
    if (i == 320):
        DISPLAYSURF.blit(background, (0, -SCREEN_HEIGHT + i))
        i = 0
    i += 10

    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Update/Re-Draw All Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collision Event Between Player & Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        pygame.mixer.Sound('./audio/crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # ------ Update Game Loop ------
    pygame.display.update()     # Every change since last refresh is updated
    FPS.tick(60)                # Lock refresh rate to 60/second