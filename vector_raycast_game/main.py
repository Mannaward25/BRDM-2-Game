import pygame as pg
import sys
from game_settings import *
from map import *
from player import *
from raycasting import *
from object_render import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:

    def __init__(self):
        # init objects
        self.map, self.player, self.ray_casting, self.object_renderer = None, None, None, None

        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = self.get_time()

        pg.mouse.set_visible(False)

        self.new_game()

    @staticmethod
    def get_time():
        return pg.time.get_ticks() * 0.001

    def new_game(self):  # object initialization
        self.map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.player = Player(self)
        self.ray_casting = RayCasting(self)

    def update(self):
        self.ray_casting.update()
        print('ok')
        pg.display.update()
        self.delta_time = self.clock.tick(FPS)
        print(self.delta_time)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        #self.map.draw()
        #self.player.draw()
        pass

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            try:
                self.check_events()
                self.time = self.get_time()

                self.update()
                self.draw()
            except ZeroDivisionError as err:
                print(f'{err.args}')
                continue


if __name__ == '__main__':
    game = Game()
    game.run()
