import pygame
import sys
from algorithm import bfs, dfs

window_width = 700
window_height = 500

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pathfinding Visualizer")

columns = 35
rows = 25

box_width = window_width // columns
box_height = window_height // rows

global grid, queue, path

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

    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


def update_grid():
    for x in range(columns):
        for y in range(rows):
            box = grid[x][y]
            box.draw(window, (44, 62, 80)) # Grigio
            
            if box.queued:
                box.draw(window, (171, 235, 198)) # Verde chiaro 
            if box.visited:
                box.draw(window, (40, 180, 99)) # Verde
            
            if box.start:
                box.draw(window, (52, 152, 219)) # Azzurro
            if box.wall:
                box.draw(window, (28, 40, 51)) # Grigio scuro
            if box.target:
                box.draw(window, (231, 76, 60)) # Rosso

            if box in path:
                box.draw(window, (244, 208, 63)) # Giallo


# Setup della griglia
for x in range(columns):
    arr = []
    for y in range(rows):
        arr.append(Cell(x, y))
    grid.append(arr)

for x in range(columns):
    for y in range(rows):
        grid[x][y].set_neighbours()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)

def main():
    start_search = False

    target_box_set = False
    target_box = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                x = mouse_x // box_width
                y = mouse_y // box_height

                if 0 <= x < columns and 0 <= y < rows and event.buttons[0]:
                    grid[x][y].wall = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                x = mouse_x // box_width
                y = mouse_y // box_height

                if 0 <= x < columns and 0 <= y < rows and event.button == 3 and not target_box_set:
                    target_box = grid[x][y]
                    target_box.target = True
                    target_box_set = True
                
                if 0 <= x < columns and 0 <= y < rows and event.button == 1:
                    grid[x][y].wall = not grid[x][y].wall

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and target_box_set:
                start_search = True

        if start_search:
            found_target = bfs(queue, path, start_box, target_box)
            if found_target:
                start_search = False

        window.fill((0, 0, 0))
        update_grid()
        pygame.display.flip()


main()
