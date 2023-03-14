import pygame as pg
import sys
from settings import *
import random
import winsound


class App:

    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(RES)
        self.fps = FPS
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.render = Renderer(self)
        #self.algorithms = Algorithms(self)
        self.algorithms = BubbleSort(self)

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.render.draw()

    def update(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()

            self.draw()
            self.algorithms.update()
            pg.display.flip()

            self.delta_time = self.clock.tick(self.fps)
            pg.display.set_caption(f"bubble_sort, fps: {self.clock.get_fps() :.1f}")


class Renderer:

    def __init__(self, main_app):
        self.app = main_app
        self.line_width = ((WIDTH - (LINES_NUM * PADDING)) / LINES_NUM)
        self.multiplier = int((HEIGHT / LINES_NUM) * HEIGHT_MAX)
        self.line_heights = [(x + 1) * self.multiplier for x in range(LINES_NUM)]

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.line_heights)

    def resize(self, line_num):
        self.multiplier = int((WIDTH / line_num) * HEIGHT_MAX)
        self.line_width = int(WIDTH / line_num)
        self.line_heights = [x * self.multiplier for x in range(line_num)]

    def draw(self):
        for k, line in enumerate(self.line_heights):
            offset = (PADDING + self.line_width) * k
            pg.draw.line(self.app.screen, pg.Color('white'), (PADDING + offset, HEIGHT - 1),
                         (PADDING + offset, (HEIGHT - 1) - line),
                         width=int(self.line_width))

    def update(self):
        pass


class Algorithms:

    def __init__(self, main_app):
        self.app = main_app
        self.total_nums = LINES_NUM
        self.initial_num = 0
        self.sorted = False

        self.lines = self.app.render.line_heights
        self.deep_copy_arr = self.lines.copy()

        self.line_width = self.app.render.line_width

    def check_sorted(self):
        is_equal = False
        for x in range(LINES_NUM):
            if sorted(self.deep_copy_arr)[x] == self.lines[x]:
                is_equal = True
            else:
                is_equal = False
                break
        return is_equal

    def go_through(self, k):
        offset = (PADDING + self.line_width) * k
        self.draw(offset, self.lines[k])

    def shuffle(self):
        random.shuffle(self.lines)

    def satollo_permutation(self):
        if self.total_nums > 1:
            self.total_nums -= 1
            j = random.randrange(0, self.total_nums)
            self.lines[j], self.lines[self.total_nums] = self.lines[self.total_nums], self.lines[j]
            self.draw(j, self.lines[j])
        else:
            self.sorted = False
            self.total_nums = len(self.lines)
            self.app.fps = FPS

    def draw(self, x, y):
        offset = (PADDING + self.line_width) * x
        #winsound.Beep(40 + y, 1)
        pg.draw.line(self.app.screen, pg.Color('red'), (PADDING + offset, HEIGHT - 1),
                     (PADDING + offset, HEIGHT - 1 - y), width=int(self.line_width))

    def update(self):
        self.go_through(self.initial_num)

        if self.initial_num < LINES_NUM - 1:
            self.initial_num += 1
        else:
            self.initial_num = 0
            self.total_nums = LINES_NUM


class BubbleSort(Algorithms):

    def __init__(self, main_app):
        super().__init__(main_app)
        self.initial_num = 0
        self.second_variable = 0

    def bubble_sort(self, k, j):
        if j < LINES_NUM - k - 1:
            if self.lines[j] > self.lines[j + 1]:
                self.lines[j], self.lines[j + 1] = self.lines[j + 1], self.lines[j]
        else:
            pass

        self.draw(j, self.lines[j])

    def update(self):
        self.bubble_sort(self.second_variable, self.initial_num)

        if not self.sorted:
            if self.initial_num < LINES_NUM - 1:
                self.initial_num += 1
            else:
                self.second_variable += 1
                self.initial_num = 0
        else:
            self.satollo_permutation()

        if self.check_sorted():
            #self.app.render.shuffle()
            self.sorted = True
            self.initial_num = 0
            self.second_variable = 0
            self.app.fps = LOW_FPS
            #self.total_nums = LINES_NUM

        # if self.sorted:
        #     self.satollo_permutation()


if __name__ == '__main__':
    app = App()
    app.update()
