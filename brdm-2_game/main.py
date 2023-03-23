import pygame as pg
import sys
from settings import *


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1

    def draw(self):
        self.screen.fill('black')

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def update(self):

        pg.display.update()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption('brdm-2 game')

    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.update()


if __name__ == '__main__':
    app = Game()
    app.run()
