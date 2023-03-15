import pygame as pg
from settings import *
import random


class Algorithms:

    def __init__(self, main_app, switch_on=True):
        self.app = main_app
        self.switch_on = switch_on
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
        pg.draw.line(self.app.screen, pg.Color('red'), (PADDING + offset, HEIGHT - 1),
                     (PADDING + offset, HEIGHT - 1 - y), width=int(self.line_width))

    def update(self):
        if self.switch_on:
            self.go_through(self.initial_num)

            if self.initial_num < LINES_NUM - 1:
                self.initial_num += 1
            else:
                self.initial_num = 0
                self.total_nums = LINES_NUM

