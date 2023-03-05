import pygame as pg
import sys
from random import random
from collections import deque
# with drawn path

# settings
COLS, ROWS = 55, 30
TILE = 20
FPS = 20

# main code


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([COLS * TILE, ROWS * TILE])
        self.clock = pg.time.Clock()

        # initialization
        self.map = Map(self)
        self.pathfind = PathFinder(self)

    def update(self):
        self.pathfind.update()

        pg.display.flip()  # pg.display.update()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')
        self.map.draw()
        self.pathfind.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            self.pathfind.click_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


class Map:
    def __init__(self, app):
        self.app = app
        self.grid = []
        self.make_grid()

    def make_grid(self):
        self.grid = [[1 if random() < 0.25 else 0 for col in range(COLS)] for row in range(ROWS)]  # 20% probability of obj
        self.grid[0][0] = 0

    def get_rect(self, x, y):
        return x * TILE, y * TILE, TILE - 2, TILE - 2

    def draw(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col:
                    pg.draw.rect(self.app.screen, pg.Color('darkorange'),
                                 self.get_rect(x, y), border_radius=TILE // 5)


class PathFinder:
    def __init__(self, app):
        self.app = app
        self.map = self.app.map
        self.grid = self.map.grid
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]

        self.graph = dict()
        self.make_adjacency_list()

        # BFS settings
        self.start = (0, 0)
        self.queue = deque([self.start])
        self.visited = {self.start: None}

        # bfs path drawing
        self.path_head, self.path_segment = self.start, self.start

        # click mouse pos target
        self.click = False
        self.x, self.y = 0, 0
        self.goal = tuple()

    def get_next_node(self, x, y) -> list:
        next_nodes = list()
        for dx, dy in self.ways:
            x_tmp, y_tmp = x + dx, y + dy
            if self.check_next_node(x_tmp, y_tmp):
                next_nodes.append((x_tmp, y_tmp))
        return next_nodes

    def check_next_node(self, x, y) -> bool:
        return True if 0 <= x < COLS and 0 <= y < ROWS and not self.grid[y][x] else False

    def get_mouse_pos(self):
        self.x, self.y = pg.mouse.get_pos()
        grid_x = self.x // TILE
        grid_y = self.y // TILE
        self.goal = (grid_x, grid_y)

        pg.draw.rect(self.app.screen, pg.Color('red'), self.map.get_rect(*self.goal))

    def make_adjacency_list(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_node(x, y)

    def bfs(self):
        self.queue = deque([self.start])
        self.visited = {self.start: None}

        while self.queue:
            cur_node = self.queue.popleft()
            self.path_head, self.path_segment = cur_node, cur_node
            if cur_node == self.goal:
                break
            next_nodes = self.graph[cur_node]
            for next_node in next_nodes:
                if next_node not in self.visited:
                    self.queue.append(next_node)
                    self.visited[next_node] = cur_node

    def click_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.click:
                self.click = True
                self.get_mouse_pos()

    def update(self):
        self.get_mouse_pos()

        if self.check_next_node(*self.goal):
            self.path_head, self.path_segment = self.goal, self.goal
            try:

                self.bfs()
            except KeyError as err:
                print(err)

    def draw(self):
        for x, y in self.visited:
            pg.draw.rect(self.app.screen, pg.Color('forestgreen'), self.map.get_rect(x, y))

        for x, y in self.queue:
            pg.draw.rect(self.app.screen, pg.Color('darkslategray'), self.map.get_rect(x, y))

        while self.path_segment:
            pg.draw.rect(self.app.screen, pg.Color('white'), self.map.get_rect(*self.path_segment),
                         TILE, border_radius=TILE // 3)
            self.path_segment = self.visited[self.path_segment]
        else:
            pg.draw.rect(self.app.screen, pg.Color('white'), self.map.get_rect(*self.path_head),
                         TILE, border_radius=TILE // 3)
            self.path_segment = self.visited[self.path_head]
            self.click = False

        pg.draw.rect(self.app.screen, pg.Color('blue'), self.map.get_rect(*self.start),
                     TILE, border_radius=TILE // 3)
        pg.draw.rect(self.app.screen, pg.Color('magenta'), self.map.get_rect(*self.path_head),
                     TILE, border_radius=TILE // 3)


if __name__ == '__main__':
    app = App()
    app.run()
