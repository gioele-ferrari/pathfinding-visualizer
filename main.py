import pygame
import sys
from utils.algorithm import bfs
from utils.colors import *

window_width = 700
window_height = 500

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pathfinding Visualizer")

columns = 35
rows = 25

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []

class Cell:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.father = None
        self.cost = 0

    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    def set_neighbours(self, grid):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


def update_cell_color():
    for x in range(columns):
        for y in range(rows):
            box = grid[x][y]
            box.draw(window, GREY_COLOR)

            if box.queued:
                box.draw(window, LIGHT_GREEN_COLOR)
            if box.visited:
                box.draw(window, GREEN_COLOR)
            if box.start:
                box.draw(window, BLUE_COLOR)
            if box.wall:
                box.draw(window, DARK_GREY_COLOR)
            if box.target:
                box.draw(window, RED_COLOR)
            if box in path:
                box.draw(window, YELLOW_COLOR)


def initialize_grid():
    global grid
    grid = [[Cell(x, y) for y in range(rows)] for x in range(columns)]
    for x in range(columns):
        for y in range(rows):
            grid[x][y].set_neighbours(grid)


initialize_grid()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)

def main():
    global start_box
    start_search = False
    target_box_set = False
    target_box = None
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gestione delle coordinate del mouse
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            x = mouse_x // box_width
            y = mouse_y // box_height

            # Sezione per la gestione del movimento del mouse
            if event.type == pygame.MOUSEMOTION:
                if 0 <= x < columns and 0 <= y < rows and event.buttons[0]:
                    grid[x][y].wall = True

            # Sezione per la gestione del click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0 <= x < columns and 0 <= y < rows and event.button == 3 and not target_box_set:
                    target_box = grid[x][y]
                    target_box.target = True
                    target_box.wall = False
                    target_box_set = True
                
                if 0 <= x < columns and 0 <= y < rows and event.button == 1:
                    grid[x][y].wall = not grid[x][y].wall

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and target_box_set:
                start_search = True
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not start_search:
                initialize_grid()
                start_box = grid[0][0]
                start_box.start = True
                start_box.visited = True
                queue.clear()
                queue.append(start_box)
                target_box_set = False

        if start_search:
            if bfs(queue, path, start_box, target_box):
                start_search = False

        window.fill((0, 0, 0))
        update_cell_color()
        pygame.display.flip()

main()
