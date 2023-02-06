import pygame as pg
import sys
import numpy as np
from settings import *


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()

    def new_app(self):
        pass

    def draw(self):
        frame = np.random.uniform(0, 1, (80, 60, 3))

        surf = pg.surfarray.make_surface(frame * 255)
        surf = pg.transform.scale(surf, RES)

        self.screen.blit(surf, (0, 0))

    def update(self):
        self.draw()
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
