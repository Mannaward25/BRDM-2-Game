import pygame as pg
import sys
from settings import *
from stacked_sprite import StackedSprite
from cache import Cache, PreloadedSprites, ByteStorage
from player import Player


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 0.01
        self.time = 0

        # groups
        self.main_group = pg.sprite.Group()
        # game objects
        self.cache = PreloadedSprites()
        self.player = Player(self)

        # scene
        StackedSprite(self, name='brdm', pos=(-WIDTH // 4, 0))
        StackedSprite(self, name='tank', pos=(WIDTH // 4, 0))

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.main_group.draw(self.screen)
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def update(self):
        self.main_group.update()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'brdm-2 game, fps: {self.clock.get_fps() :.1f}')

    def run(self):
        while True:
            self.check_events()
            self.get_time()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = Game()
    app.run()
