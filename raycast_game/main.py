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

# npc movement algorithm (npc.py)
# npc ray cast algorithm (npc.py)
# npc path finding algorithm (pathfinding.py)
# npc run_logic review (npc.py)
# global trigger sense (main.py)
# breadth first search algorithm (in pathfinding.py)
# player interactions (get_damage, digits object_render.py)


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.time = self.get_time()

        self.global_trigger = False  # special global event for npc animation
        self.global_event = pg.USEREVENT + 0  # special global event for npc animation
        pg.time.set_timer(self.global_event, 40)  # special global event for npc animation

        self.new_game()
        pg.mouse.set_visible(False)

    @staticmethod
    def get_time():
        return pg.time.get_ticks() * 0.001

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.doom_fire = DoomFire(self)
        self.object_renderer = ObjectRenderer(self)
        self.mode7 = Mode7(self)
        self.raycasting = RayCasting(self)

        # self.static_sprite = SpriteObject(self) # old way of rendering sprite objects
        # self.animated_sprite = AnimatedSprite(self)

        # new way of rendering sprite objects
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)

        # pg.mixer.music.load(self.sound.path + f'theme{randint(1, 3)}.mp3')  #  uncomment to play
        # pg.mixer.music.play()

    def update(self):
        self.player.update()
        self.mode7.update()  # working
        self.raycasting.update()  # working
        # self.static_sprite.update()
        # self.animated_sprite.update()
        self.object_handler.update() # working
        self.weapon.update()  # working
        #self.doom_fire.update()  # working

        pg.display.update()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        #self.screen.fill(BLACK)
        self.mode7.draw()  # working
        self.object_renderer.draw()
        self.weapon.draw()
        #self.doom_fire.draw()

        #self.map.draw()  # working
        #self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            try:
                self.check_events()
                self.time = self.get_time()
                self.update()
                self.draw()
            except ZeroDivisionError as err:
                print(f'{err}')
                continue


if __name__ == '__main__':
    game = Game()
    game.run()
