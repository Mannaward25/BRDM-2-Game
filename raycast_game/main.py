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
from network_game import Client
from menu import MenuManager
import subprocess
import time


class Game:  # +

    def __init__(self, host=False, network_game=False):  # +
        pg.init()  # +
        self.screen = pg.display.set_mode(RES)  # +
        self.clock = pg.time.Clock()  # +
        self.delta_time = 1  # +
        self.time = self.get_time()

        self.global_trigger = False  # special global event for npc animation
        self.global_event = pg.USEREVENT + 0  # special global event for npc animation
        pg.time.set_timer(self.global_event, 40)  # special global event for npc animation

        # menu settings
        self.background = pg.Surface(RES)
        self.menu_flag = True
        self.game_start_flag = False
        self.game_pause_flag = False
        self.no_npc = False
        self.no_sound = False
        self.network_game = network_game
        self.HOST = host
        self.server_address = ''
        path = 'resources/pics/main.jpg'
        self.bg_menu_img = pg.image.load(path).convert_alpha()
        pg.transform.scale(self.bg_menu_img, RES)
        self.menu_manager = MenuManager(self)

        # network settings
        self.clients = 0
        self.client = None
        self.exec_path = sys.executable

        self.new_game()  # +

    @staticmethod
    def get_time():
        return pg.time.get_ticks() * 0.001

    def new_game(self):  # +
        if self.network_game:
            self.client = Client(self, server=self.server_address)

        self.map = Map(self)  # +
        self.player = Player(self)  # +
        #self.doom_fire = DoomFire(self)
        self.object_renderer = ObjectRenderer(self)  # +
        #self.mode7 = Mode7(self)
        self.raycasting = RayCasting(self)  # +

        # new way of rendering sprite objects
        self.object_handler = ObjectHandler(self, no_npc=self.no_npc)
        self.weapon = Weapon(self)

        self.sound = Sound(self, no_sound=self.no_sound)
        if not self.game_start_flag:
            self.sound.main_menu()
        else:
            self.sound.main_game()

        self.pathfinding = PathFinding(self)
        self.mode_seven = FakeModeSeven(self)

    def update(self):  # +
        #self.mode7.update()  # working
        self.raycasting.update()  # working
        self.player.update()

        self.object_handler.update()  # working
        self.weapon.update()  # working
        #self.doom_fire.update()  # working
        #self.mode_seven.update()

        pg.display.update()
        self.delta_time = self.clock.tick(FPS)

        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill(BLACK)
        #self.mode7.draw()  # working
        self.object_renderer.draw()
        self.weapon.draw()
        #self.doom_fire.draw()
        #self.map.draw()  # working
        #self.player.draw()

    def draw_menu(self):
        self.background.fill('dark green')
        self.screen.blit(self.bg_menu_img, (0, 0))
        self.menu_manager.draw()

    def update_menu(self):
        pg.display.update()
        self.delta_time = self.clock.tick(FPS)
        self.menu_manager.update(self.delta_time)
        pg.display.set_caption(f'menu app')

    def check_events(self):  # +
        self.global_trigger = False  # +
        for event in pg.event.get():  # +
            if event.type == pg.QUIT: #  (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)

                if self.HOST:
                    self.client.send_msg(CLOSE)
                    self.client.close()

                pg.quit()  # +
                sys.exit()  # +

            elif event.type == self.global_event:  # +
                self.global_trigger = True  # +

            elif event.type == pg.KEYDOWN and event.key in (pg.K_w, pg.K_a, pg.K_s, pg.K_d):
                self.player.is_walking = True
            elif event.type == pg.KEYUP and event.key in (pg.K_w, pg.K_a, pg.K_s, pg.K_d):
                self.player.is_walking = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and self.game_start_flag and not self.menu_flag:
                print('main menu')
                self.menu_manager.game_pause()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and self.game_start_flag and self.menu_flag:
                self.menu_manager.resume_game()

            if self.game_start_flag and not self.game_pause_flag:
                self.player.single_fire_event(event)  # +

            self.menu_manager.menu_events(event)

    def run(self):  # +
        while True:  # +
            try:  # +
                self.check_events()  # +
                self.time = self.get_time()  # +

                if self.menu_flag:
                    pg.mouse.set_visible(True)
                    self.draw_menu()
                    self.update_menu()
                else:
                    pg.mouse.set_visible(False)  # +
                    self.update()  # +
                    self.draw()  # +
            except ZeroDivisionError as err:  # +
                print(f'{err}')  # +
                continue  # +


if __name__ == '__main__':  # +
    game = Game(host=False, network_game=False)  # +
    game.run()  # +
