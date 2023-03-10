import pygame as pg
import sys
from settings import *

from editor import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        # initialization
        self.editor = Editor(self)

    def game_init(self):
        pass
    
    def update(self):
        pg.display.update()
        self.delta_time = self.clock.tick(FPS)

        self.editor.update(self.delta_time)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.editor.draw()

    def run(self):
        while True:
            self.update()
            self.draw()

    
if __name__ == '__main__':
    app = Game()
    app.run()
    