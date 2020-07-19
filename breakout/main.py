import pygame
import pygame.gfxdraw
from pygame.locals import *

import random
import math

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

# ================= CONSTANTS ======================

BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
DARKBLUE = (47, 105, 130) 
GREEN = (64, 242, 19) 
BLUE = (19, 64, 242) 
VIOLET = (151, 42, 201)
GRAY = (192, 192, 192)
LIGHTGREEN = (0, 255, 195)
CYAN = (45, 189, 165)
CRIMSON = (199, 20, 49)

_COLORS = [DARKBLUE, BLUE, VIOLET, CYAN, (0, 250, 167), (246, 250, 0)]



BRICK_HEIGHT = 10
BRICK_WIDTH = 40

PLATFORM_HEIGHT = 10
PLATFORM_WIDTH = 80

BALL_RADIUS = 15

# the rectangle in which all the bricks are placed
BRICKS_ROWS = 20
BRICK_COLS = 15

FREE_AREA = 200 # area between bricks and platform
TOP_AREA = 100 # area between upper wall and bricks

SCREEN_HEIGHT = BRICKS_ROWS * BRICK_HEIGHT + FREE_AREA + TOP_AREA
SCREEN_WIDTH = BRICK_COLS * BRICK_WIDTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ================= CONSTANTS ======================

# a brick to be breaked by that ball
class Brick(pygame.sprite.Sprite):
    def __init__(self, top, left):
        super(Brick, self).__init__()
        self.surf = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.rect = self.surf.get_rect(topleft=(top, left))
        self.surf.fill(random.choice(_COLORS))
    
    def update(self):
        pass
    
# the thing which keeps the ball above from the ground
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.surf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = self.surf.get_rect(topleft=((SCREEN_WIDTH - PLATFORM_WIDTH) // 2, SCREEN_HEIGHT - PLATFORM_HEIGHT))
        self.surf.fill(GRAY)
        self.speed = 3
        
    def update(self, pressed_key):
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_key[K_RIGHT]: 
            self.rect.move_ip(self.speed, 0)
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH   
    
# a ball which moves and reflect from the walls and bricks
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        
        self.surf = pygame.Surface([BALL_RADIUS, BALL_RADIUS])
        self.surf.fill(WHITE)
        pygame.draw.circle(self.surf, BLACK, (BALL_RADIUS // 2, BALL_RADIUS // 2), BALL_RADIUS // 2)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLATFORM_HEIGHT - BALL_RADIUS // 2))
        self.dx = random.choice([-1, 1])
        self.dy = 1
    
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
   
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx *= -1
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.dx *= -1
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dy *= -1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
            global game_over
            game_over = True
            self.kill()
            
        collision = pygame.sprite.spritecollideany(_ball, [_platform])
        if collision:
            if collision == _platform:
                self.rect.y -= self.dy
                self.dy *= -1
        
        collide = pygame.sprite.spritecollideany(_ball, bricks_group)
        if collide:
            collide.kill()
            self.rect.y -= self.dy
            self.dy *= -1
            
            global score
            score += 1
            
            if score > 30:
                self.dx = 2
                self.dy = 2
            if score > 60:
                self.dx = 3
                self.dy = 3
            if score > 100:
                self.dx = 4
                self.dy = 4
            



# =============== HELPER FUNCTIONS ===================

def new_game():
    global _platform
    global _ball
    global bricks_group
    global all_sprites
    _platform = Platform()
    _ball = Ball()

    bricks_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    all_sprites.add(_ball)
    all_sprites.add(_platform)

    for i in range(BRICKS_ROWS):
        for j in range(BRICK_COLS):
            brick = Brick(i * BRICK_WIDTH, j * BRICK_HEIGHT + TOP_AREA)
            bricks_group.add(brick)
            all_sprites.add(brick)

# =============== HELPER FUNCTIONS ===================

# ============ SPRITE GROUPS =========================

_ball = None
_plaform = None
bricks_group = all_sprites = None

# ============ SPRITE GROUPS =========================


running = True
pause = True

new_game()
wins = False
game_over = False
score = 0
new_games = True

while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key == K_p:
                pause = True
            if event.key == K_r:
                pause = False
            
            if new_games or game_over or wins or pause:
                if event.key == K_n:
                    new_game()
                    score = 0
                    wins = False
                    new_games = False
                    game_over = False
                    pause = False
                
                    
    if new_games:
        screen.fill(WHITE)
        font = pygame.font.Font('breakout\ARCADECLASSIC.TTF', 60)
        textsurface = font.render(f"NEW GAME", True, BLACK)
        screen.blit(textsurface, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 60))
        font = pygame.font.Font('breakout\ARCADECLASSIC.TTF', 20)
        pressr = font.render("Press N to start", True, BLACK)
        screen.blit(pressr, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 + 50))
    else:
        if not pause:
            pressed_key = pygame.key.get_pressed()
            _platform.update(pressed_key)
            _ball.update()
            
            if score == BRICK_COLS * BRICKS_ROWS:
                wins = True
                pause = True
    
        screen.fill(WHITE)
            
        font = pygame.font.Font('breakout\ARCADECLASSIC.TTF', 30)
        textsurface = font.render(f"SCORE {score}", True, BLACK)
        screen.blit(textsurface, (10, 10))
        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        if game_over:
            screen.fill(WHITE)
            font = pygame.font.Font('breakout\ARCADECLASSIC.TTF', 60)
            textsurface = font.render(f"GAME over", True, BLACK)
            screen.blit(textsurface, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 60))
            font = pygame.font.Font('breakout\ARCADECLASSIC.TTF', 20)
            pressr = font.render("Press N for a new game", True, BLACK)
            screen.blit(pressr, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
        
        if wins:
            screen.fill(WHITE)
            font = pygame.font.Font('breakout\ARCADECLASSIC.TTF', 60)
            textsurface = font.render(f"YOU WIN", True, BLACK)
            screen.blit(textsurface, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 60))
            font = pygame.font.Font('breakout\ARCADECLASSIC.TTF', 20)
            pressr = font.render("Press N for a new game", True, BLACK)
            screen.blit(pressr, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
        
        if pause:
            screen.fill(WHITE)
            font = pygame.font.Font('breakout\ARCADECLASSIC.TTF', 50)
            paused = font.render(f"PAUSED", True, BLACK)
            screen.blit(paused, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 60))
            font = pygame.font.Font('breakout\ARCADECLASSIC.TTF', 20)
            pressr = font.render("Press R to Resume", True, BLACK)
            screen.blit(pressr, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 + 50))
        
    clock.tick(180)
    pygame.display.flip()