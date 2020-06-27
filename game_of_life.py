import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)

ROWS = 50
COLS = 50
CELL_HEIGHT = 10
CELL_WIDTH = CELL_HEIGHT
SCREEN_WIDTH = CELL_HEIGHT * COLS
SCREEN_HEIGHT = CELL_HEIGHT * ROWS

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# represent a cell
class Cell(pygame.sprite.Sprite):
    def __init__(self, top, left):
        super(Cell, self).__init__()
        self.surf = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(topleft=(top, left))
        self.alive = False

    def update(self, alive):
        self.alive = alive
        if self.alive:
            self.surf.fill(BLACK)
        else:
            self.surf.fill(WHITE)


cell_grid = [[Cell(i * CELL_HEIGHT, j * CELL_HEIGHT) for j in range(COLS)] for i in range(ROWS)]
masked_grid = [[0 for j in range(COLS)] for i in range(ROWS)]
neighbors = [[0 for j in range(COLS)] for i in range(ROWS)]



def get_alive_neighbors(masked_grid, row, col):
    count = 0
    if (0 <= row-1 < ROWS) and masked_grid[row-1][col] == 1: 
        count += 1
    if (0 <= row+1 < ROWS) and masked_grid[row+1][col] == 1: 
        count += 1
    if (0 <= col-1 < COLS) and masked_grid[row][col-1] == 1: 
        count += 1
    if (0 <= col+1 < COLS) and masked_grid[row][col+1] == 1: 
        count += 1
    
    if (0 <= row-1 < ROWS) and (0 <= col-1 < COLS) and masked_grid[row-1][col-1] == 1: 
        count += 1
    if (0 <= row-1 < ROWS) and (0 <= col+1 < COLS) and masked_grid[row-1][col+1] == 1: 
        count += 1
    if (0 <= row+1 < ROWS) and (0 <= col-1 < COLS) and masked_grid[row+1][col-1] == 1: 
        count += 1
    if (0 <= row+1 < ROWS) and (0 <= col+1 < COLS) and masked_grid[row+1][col+1] == 1: 
        count += 1
    return count

def get_cell_location(x, y):
    row = int(x / CELL_HEIGHT)
    col = int(y / CELL_HEIGHT)
    return row, col

def set_alive(masked_grid, x, y):
    row, col = get_cell_location(x, y)
    masked_grid[row][col] = 1

def set_dead(masked_grid, x, y):
    row, col = get_cell_location(x, y)
    masked_grid[row][col] = 0
    
def copy(new_grid):
    grid = [[0 for j in range(COLS)] for i in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            grid[i][j] = new_grid[i][j]
    return grid

def update_masked_grid(masked_grid):
    copy_grid = copy(masked_grid)
    for i in range(ROWS):
        for j in range(COLS):
            alive = (masked_grid[i][j] == 1)
            live_neighbors = get_alive_neighbors(masked_grid, i, j)
            neighbors[i][j] = live_neighbors
            if alive and (live_neighbors < 2 or live_neighbors > 3):
                copy_grid[i][j] = 0
            if not alive and live_neighbors == 3:
                copy_grid[i][j] = 1
    for i in range(ROWS):
        for j in range(COLS):
            masked_grid[i][j] = copy_grid[i][j]
                

def update_cell_grid(cell_grid, masked_grid):
    for i in range(ROWS):
        for j in range(COLS):
            cell_grid[i][j].update(True if masked_grid[i][j] == 1 else False)
        
    
grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

cell_grid_sprites = pygame.sprite.Group()
for i in range(ROWS):
    for j in range(COLS):
        cell_grid_sprites.add(cell_grid[i][j])

running = True
pause = True
while running:

    # event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pause = not pause

    # fill screen with white color
    screen.fill(WHITE)
    
    if pause:
        if pygame.mouse.get_pressed()[0] == 1:
            set_alive(masked_grid, *pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[2] == 1:
            set_dead(masked_grid, *pygame.mouse.get_pos())
    else:
        update_masked_grid(masked_grid)

    update_cell_grid(cell_grid, masked_grid)
    
    for entity in cell_grid_sprites:
        screen.blit(entity.surf, entity.rect)
    
    for i in range(ROWS):
        pygame.draw.line(screen, GRAY, (0, CELL_HEIGHT * i), (SCREEN_WIDTH, CELL_HEIGHT * i), 1)
    for i in range(COLS):
        pygame.draw.line(screen, GRAY, (CELL_HEIGHT * i, 0), (CELL_HEIGHT * i, SCREEN_HEIGHT), 1)

    pygame.display.flip()
    
    clock.tick(30)

pygame.quit()