import pygame as pg
import sys
from settings import *
from typing import Any


class Button:

    def __init__(self, parent, text,  pos=(0, 0), size=(260, 40), center=True, btn_id=0):
        self.menu = parent
        self.font = parent.font
        self.text = text
        self.btn_id = btn_id

        self.pos = pos
        self.relative_position()
        self.size = size
        self.center = center

        self.btn: pg.Rect = pg.rect.Rect(self.pos, self.size)

    def get_size(self):
        return self.size

    def get_pos(self):
        return self.pos

    def move(self, x, y):
        self.pos = (x, y)

    def check_collision(self) -> callable:
        mouse_pos = pg.mouse.get_pos()

        if self.btn.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0] and self.menu.visible:
            print(f'pressed button {self.text}')
            return self.btn_id

    def relative_position(self):
        x_pos, y_pos = self.pos
        menu_w, menu_h = self.menu.get_pos()
        new_pos_x, new_pos_y = menu_w + x_pos, menu_h + y_pos
        self.pos = new_pos_x, new_pos_y

    def center_position(self):
        x_size, y_size = self.size
        x_pos, y_pos = self.pos
        menu_w, menu_h = self.menu.get_pos()
        pad_x = (menu_w + (menu_w + x_size)) // 2
        self.pos = pad_x, y_pos

    def draw(self):

        x_pos, y_pos = self.pos
        x_size, y_size = self.size

        if self.center:
            self.center_position()

        self.btn = pg.draw.rect(self.menu.screen, 'gray', ((x_pos, y_pos), self.size), border_radius=5)
        pg.draw.rect(self.menu.screen, 'black', ((x_pos, y_pos), self.size), width=3, border_radius=5)
        text = self.font.render(self.text, True, 'black')
        self.menu.screen.blit(text, (x_pos + (x_size // 4), y_pos + ((y_size - FONT_SIZE) // 2)))

    def update(self):
        self.draw()


class Menu:

    def __init__(self, app, visible=False):
        self.app = app
        self.screen = self.app.screen
        self.font = pg.font.Font('freesansbold.ttf', FONT_SIZE)

        self.menu_width = 500
        self.menu_height = 500
        self.menu_pos = self.calc_sizes()
        self.menu_frame = pg.rect.Rect(INIT_RECT)

        self.visible = visible
        self.button_option = 0
        self.btn_list = []

    def get_size(self):
        return self.menu_width, self.menu_height

    def get_pos(self):
        return self.menu_pos

    def set_visible(self, flag):
        self.visible = flag

    def calc_sizes(self):
        margin_hor = (WIDTH - self.menu_width) // 2
        margin_vert = (HEIGHT - self.menu_height) // 2
        self.menu_pos = margin_hor, margin_vert
        return margin_hor, margin_vert

    def check_event(self):
        for btn in self.btn_list:
            opt = btn.check_collision()
            if opt:
                self.button_option = opt
                break

    def get_option(self):
        return self.button_option

    def draw(self):
        marg_x, marg_y = self.menu_pos
        pg.draw.rect(self.screen, 'black', (marg_x, marg_y, self.menu_width, self.menu_height), width=2)

    def update(self):
        self.draw()


class MainMenu(Menu):

    def __init__(self, app, visible=True):
        super().__init__(app, visible)

        self.menu_btn: Button = Button(self, 'Play single', pos=(100, 100), btn_id=1)
        self.multiplayer_btn: Button = Button(self, 'Multiplayer', pos=(100, 150), btn_id=2)
        self.settings_btn: Button = Button(self, 'Settings', pos=(100, 200), btn_id=3)
        self.quit_btn: Button = Button(self, 'Quit', pos=(100, 250), btn_id=4)

        self.btn_list = self.get_buttons()

    def get_buttons(self):
        return [self.menu_btn, self.multiplayer_btn, self.settings_btn, self.quit_btn]

    def update(self):
        super().update()
        self.menu_btn.update()
        self.multiplayer_btn.update()
        self.settings_btn.update()
        self.quit_btn.update()


class MultiplayerMenu(Menu):

    def __init__(self, app, visible=True):
        super().__init__(app, visible)
        self.connect_btn: Button = Button(self, 'Connect', pos=(100, 100), btn_id=5)
        self.back_btn: Button = Button(self, 'Back', pos=(100, 150), btn_id=6)

        self.btn_list = self.get_buttons()

    def get_buttons(self):
        return [self.connect_btn, self.back_btn]

    def update(self):
        super().update()
        self.connect_btn.update()
        self.back_btn.update()


class MenuRenderer:

    def __init__(self, app):
        self.app = app
        self.menu = MainMenu(self.app)
        self.multiplayer_menu = MultiplayerMenu(self.app, visible=DISABLE)
        self.menu_to_render = None

        self.init_menu()

        self.switch_menu = {
            0: False,
            1: self.menu,
            2: self.multiplayer_menu,
            3: self.menu,
            4: self.quit,
            5: self.multiplayer_menu,
            6: self.menu
        }

    def choose_menu(self):
        self.menu_to_render.check_event()
        opt = self.menu_to_render.get_option()
        self.menu_to_render.set_visible(DISABLE)
        self.menu_to_render = self.switch_menu[opt]
        if self.menu_to_render and not callable(self.menu_to_render):
            self.menu_to_render.set_visible(ENABLE)
        elif self.menu_to_render and callable(self.menu_to_render):
            self.menu_to_render()

    def init_menu(self):
        self.menu_to_render = self.menu

    def render(self):
        if self.menu_to_render:
            self.menu_to_render.update()

    def quit(self):
        pg.quit()
        sys.exit()


class App:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.menu_render = MenuRenderer(self)

    def draw(self):
        self.screen.fill('dark green')

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.menu_render.choose_menu()
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                pass

    def update(self):
        self.menu_render.render()

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'menu app')

    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.update()


if __name__ == '__main__':
    main_app = App()
    main_app.run()
