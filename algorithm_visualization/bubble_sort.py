from algortims import Algorithms
from settings import *


class BubbleSort(Algorithms):

    def __init__(self, main_app, switch_on=True):
        super().__init__(main_app, switch_on)
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
        if self.switch_on:
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



