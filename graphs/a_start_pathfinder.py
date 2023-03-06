import heapq
import math

import pygame as pg
import sys
from random import random
from collections import deque
# general case pathfinder visualization

# settings
COLS, ROWS = 25, 15
TILE = 40
FPS = 60

MULT_K = 10

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
        self.start_graph = dict()
        self.make_adjacency_list()

        # a star settings
        self.start = (0, 0)
        self.goal = self.start
        self.queue = []
        self.visited = {self.start: None}
        self.cost_visited = {self.start: 0}

        heapq.heappush(self.queue, (0, self.start))
        self.path_head, self.path_segment = self.start, self.start
        self.cur_node = self.start

        # mouse settings
        self.click = False

    def reset_params(self):
        self.graph = self.start_graph.copy()
        self.queue = []
        self.visited = {self.start: None}
        self.cost_visited = {self.start: 0}
        heapq.heappush(self.queue, (0, self.start))
        self.path_head, self.path_segment = self.start, self.start
        self.cur_node = self.start

    def get_next_node(self, x, y) -> list:
        next_nodes = list()
        weight = 0
        for dx, dy in self.ways:
            x_tmp, y_tmp = x + dx, y + dy
            if self.check_next_node(x_tmp, y_tmp):
                next_nodes.append(((x_tmp, y_tmp), weight))
        return next_nodes

    def check_next_node(self, x, y) -> bool:
        return True if 0 <= x < COLS and 0 <= y < ROWS and not self.grid[y][x] else False

    def make_adjacency_list(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_node(x, y)

        self.start_graph = self.graph.copy()

    @staticmethod
    def pythagorean(dx, dy):
        res = math.sqrt(abs(dx * dx) + abs(dy * dy))
        return res

    def calc_adjacent_weights(self, x, y):  # x, y of cur_node (start)
        next_nodes = list()
        for dx, dy in self.ways:
            x_tmp, y_tmp = x + dx, y + dy
            if self.check_next_node(x_tmp, y_tmp):
                h_cost = self.calc_heuristic(x_tmp, y_tmp)
                if all([dx, dy]):
                    next_nodes.append(((x_tmp, y_tmp), int(self.pythagorean(dx, dy) * MULT_K) + h_cost))
                else:
                    next_nodes.append(((x_tmp, y_tmp), MULT_K + h_cost))

        self.graph[(x, y)] = next_nodes

    def calc_heuristic(self, x, y):  # x, y of adjacent point
        x_goal, y_goal = self.goal
        diff_x, diff_y = x_goal - x, y_goal - y
        h_cost = self.pythagorean(diff_x, diff_y)
        return int(h_cost)

    def get_mouse_pos(self):
        x, y = pg.mouse.get_pos()
        grid_x = x // TILE
        grid_y = y // TILE
        self.goal = (grid_x, grid_y)

        pg.draw.rect(self.app.screen, pg.Color('red'), self.map.get_rect(*self.goal))

    def a_start_algorithm(self):  # dijkstra
        if self.queue:
            cur_cost, cur_node = heapq.heappop(self.queue)
            self.calc_adjacent_weights(*cur_node)
            self.path_head, self.path_segment = cur_node, cur_node
            self.cur_node = cur_node

            next_nodes = self.graph[cur_node]
            for next_node in next_nodes:
                neigh_node, neigh_cost = next_node
                new_cost = self.cost_visited[cur_node] + neigh_cost

                if neigh_node not in self.cost_visited or new_cost < self.cost_visited[neigh_node]:
                    heapq.heappush(self.queue, (new_cost, neigh_node))
                    self.cost_visited[neigh_node] = new_cost
                    self.visited[neigh_node] = cur_node

    def click_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.click:
                self.click = True
                self.reset_params()

    def update(self):
        if self.click:
            self.get_mouse_pos()
            self.click = False

        x, y = self.goal
        if self.cur_node != self.goal and not self.grid[y][x]:
            self.a_start_algorithm()


    def draw(self):
        for x, y in self.visited:
            pg.draw.rect(self.app.screen, pg.Color('forestgreen'), self.map.get_rect(x, y))

        for cost, coord in self.queue:
            x, y = coord
            pg.draw.rect(self.app.screen, pg.Color('darkslategray'), self.map.get_rect(x, y))

        while self.path_segment:
            pg.draw.rect(self.app.screen, pg.Color('white'), self.map.get_rect(*self.path_segment),
                         TILE, border_radius=TILE // 3)
            self.path_segment = self.visited[self.path_segment]
        else:
            pg.draw.rect(self.app.screen, pg.Color('white'), self.map.get_rect(*self.path_head),
                         TILE, border_radius=TILE // 3)
            self.path_segment = self.visited[self.path_head]


if __name__ == '__main__':
    app = App()
    app.run()
