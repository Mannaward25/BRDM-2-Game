import pygame as pg
import sys
from settings import *
import random
from bubble_sort import BubbleSort
from fire import DoomFire


class App:

    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(RES)
        self.fps = FPS
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.render = Renderer(self, switch_on=False)
        self.algorithms = BubbleSort(self, switch_on=False)
        self.fire = DoomFire(self, switch_on=True)

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.render.draw()
        self.fire.draw()

    def update(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()

            self.algorithms.update()
            self.fire.update()
            self.draw()
            pg.display.flip()

            self.delta_time = self.clock.tick(self.fps)
            pg.display.set_caption(f"bubble_sort, fps: {self.clock.get_fps() :.1f}")


class Renderer:

    def __init__(self, main_app, switch_on=True):
        self.app = main_app
        self.switch_on = switch_on
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
        if self.switch_on:
            for k, line in enumerate(self.line_heights):
                offset = (PADDING + self.line_width) * k
                pg.draw.line(self.app.screen, pg.Color('white'), (PADDING + offset, HEIGHT - 1),
                             (PADDING + offset, (HEIGHT - 1) - line),
                             width=int(self.line_width))


if __name__ == '__main__':
    app = App()
    app.update()
