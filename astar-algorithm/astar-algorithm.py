import pygame
from pygame.locals import *

from grid import Grid
from algorithm import AStarAlgorithm

pygame.init()
clock = pygame.time.Clock()


# =============== CONSTANTS ======================

WHITE = (255, 255, 255) # for free space
DARKBLUE = (47, 105, 130) # for obstacles
GREEN = (64, 242, 19) # for begin location
BLUE = (19, 64, 242) # for end location
VIOLET = (151, 42, 201)
GRAY = (192, 192, 192)
LIGHTGREEN = (0, 255, 195)
CYAN = (45, 189, 165)


ROWS = 50
COLS = 50
CELL_HEIGHT = 10
CELL_WIDTH = CELL_HEIGHT
SCREEN_WIDTH = CELL_HEIGHT * COLS
SCREEN_HEIGHT = CELL_HEIGHT * ROWS

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# =============== CONSTANTS ======================

# represent a cell in the game
class Cell(pygame.sprite.Sprite):
    def __init__(self, top, left):
        super(Cell, self).__init__()
        self.surf = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(topleft=(top, left))
        self.begin = False
        self.obstacle = False
        self.end = False
        self.traversed = False
        self.path = False
    
    def update(self, set_mode: str):
        if set_mode == 'begin':
            self.begin = True
            self.obstacle = self.end = False
            self.surf.fill(VIOLET)
        
        if set_mode == 'end':
            self.end = True
            self.obstacle = self.begin = False
            self.surf.fill(BLUE)
        
        if set_mode == 'obstacle':
            self.obstacle = True
            self.begin = self.end = False
            self.surf.fill(DARKBLUE)
            
        if set_mode == 'path':
            self.path = True
            self.surf.fill(LIGHTGREEN)
        
        if set_mode == 'free':
            self.begin = self.end = self.obstacle = False
            self.surf.fill(WHITE)
            
# =============== GLOBALS =========================

# initializing grid
masked_grid = Grid[int](ROWS, COLS, 0)

# initializing cell grid which used to display cells on the screen
cell_grid = [[Cell(i * CELL_HEIGHT, j * CELL_HEIGHT) for j in range(COLS)] for i in range(ROWS)]

# a start point
begin = (0, 0)

# a end point
end = (ROWS - 1, COLS - 1)

# path containing points in the form (x, y)
path = []

# cell grid sprites to update the view
cell_grid_sprites = pygame.sprite.Group()
for i in range(ROWS):
    for j in range(COLS):
        cell_grid_sprites.add(cell_grid[i][j])

# =============== GLOBALS =========================
            
# =================================================

def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(screen, GRAY, (0, CELL_HEIGHT * i), (SCREEN_WIDTH, CELL_HEIGHT * i), 1)
    for i in range(COLS):
        pygame.draw.line(screen, GRAY, (CELL_HEIGHT * i, 0), (CELL_HEIGHT * i, SCREEN_HEIGHT), 1)

def clear_cell_grid():
    for i in range(ROWS):
        for j in range(COLS):
            cell_grid[i][j].update('free')
    
def update_path(path):
    for i in range(ROWS):
        for j in range(COLS):
            if cell_grid[i][j].path:
                cell_grid[i][j].surf.fill(CYAN)
                cell_grid[i][j].path = False
    # print("DEBUG : [len(path)] ", len(path))
    for point in path:
        if point is None:
            continue
        row, col = point.x, point.y
        cell_grid[row][col].update('path')
    

def get_cell_location(x, y):
    row = int(x / CELL_HEIGHT)
    col = int(y / CELL_HEIGHT)
    return row, col

def set_obstacle(x, y):
    row, col = get_cell_location(x, y)
    masked_grid[row][col] = 1
    cell_grid[row][col].update('obstacle')

def unset_obstacle(x, y):
    row, col = get_cell_location(x, y)
    masked_grid[row][col] = 0
    cell_grid[row][col].update('free')

def set_begin(x, y):
    row, col = get_cell_location(x, y)
    global begin
    prev_row, prev_col = begin
    begin = (row, col)
    cell_grid[prev_row][prev_col].update('free')
    cell_grid[row][col].update('begin')

def set_end(x, y):
    row, col = get_cell_location(x, y)
    global end
    prev_row, prev_col = end
    end = (row, col)
    cell_grid[prev_row][prev_col].update('free')
    cell_grid[row][col].update('end')

# =================================================


running = True
pause = True

begin_mode = True
end_mode = False
obstacle_mode = False

algorithm = AStarAlgorithm(masked_grid, begin, end)
runner = None
while running:
    
    # event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pause = not pause

            print("DEBUG : [pause] ", pause)
            print("DEBUG : [begin] ", begin)
            print("DEBUG : [end] ", end)
            if pause:
                if event.key == K_b:
                    print("DEBUG : [begin_mode] ", begin_mode)
                    begin_mode = True
                    end_mode = obstacle_mode = False
                if event.key == K_e:
                    print("DEBUG : [end_mode] ", end_mode)
                    end_mode = True
                    begin_mode = obstacle_mode = False
                if event.key == K_o:
                    print("DEBUG : [obstacle_mode] ", obstacle_mode)
                    obstacle_mode = True
                    end_mode = begin_mode = False
                if event.key == K_c:
                    masked_grid = Grid[int](ROWS, COLS, 0)
                    clear_cell_grid()
            else:
                algorithm = AStarAlgorithm(masked_grid, begin, end)
                runner = algorithm.run()
                
    
    # fill screen with white color
    screen.fill(WHITE)
    
    if pause:
        if begin_mode:
            if pygame.mouse.get_pressed()[0] == 1:
                set_begin(*pygame.mouse.get_pos())
        if end_mode:
            if pygame.mouse.get_pressed()[0] == 1:
                set_end(*pygame.mouse.get_pos())
        if obstacle_mode:
            if pygame.mouse.get_pressed()[0] == 1:
                set_obstacle(*pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[2] == 1:
                unset_obstacle(*pygame.mouse.get_pos())
    else:
        try:
            path = next(runner)
            update_path(path)
        except StopIteration:
            pause = True
                
    # update_cell_grid()
    for entity in cell_grid_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # draw_grid()
    pygame.display.flip()
    
    clock.tick(30)
    

pygame.quit()
