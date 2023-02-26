import pygame as pg
import sys
from settings import *
from object_render import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        # initialization
        self.object_renderer: ObjectRender = ObjectRender(self)

    def update(self):
        pg.display.update()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill(BLACK)
        self.object_renderer.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT \
                    or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = Game()
    app.run()
