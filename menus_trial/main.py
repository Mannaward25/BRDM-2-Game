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


class QuitMenu(Menu):

    def __init__(self, app, visible=True):
        super().__init__(app, visible)
        self.yes_btn: Button = Button(self, 'Yes', pos=(100, 100), btn_id=7)
        self.no_btn: Button = Button(self, 'No', pos=(100, 150), btn_id=8)

        self.btn_list = self.get_buttons()

    def get_buttons(self):
        return [self.yes_btn, self.no_btn]

    def update(self):
        super().update()
        self.yes_btn.update()
        self.no_btn.update()


class GamePause(Menu):

    def __init__(self, app, visible=True):
        super().__init__(app, visible)
        self.continue_btn: Button = Button(self, 'Continue', pos=(100, 100), btn_id=9)
        self.quit_btn: Button = Button(self, 'Quit Game', pos=(100, 150), btn_id=4)

        self.btn_list = self.get_buttons()

    def get_buttons(self):
        return [self.continue_btn, self.quit_btn]

    def update(self):
        super().update()
        self.continue_btn.update()
        self.quit_btn.update()


class ContextNode:

    def __init__(self, menu, node=None):
        self.data = menu
        self.prev = node


class MenuHistory:

    def __init__(self):
        self.head = None
        self.cur = None

    def add(self, data):
        if not self.head:
            self.head = ContextNode(data)
            self.cur = self.head
        else:
            prev = self.cur
            self.cur = ContextNode(data, prev)

    def get_prev(self):
        return self.cur.prev.data

    def show_all(self):
        node = self.cur
        count = 0
        while node:
            print(count, node.data)
            count += 1
            node = node.prev

    def clear(self):
        self.head = self.cur
        self.cur = None


class MenuRenderer:

    def __init__(self, app):
        self.app = app
        self.screen = app.screen

        self.menu = MainMenu(self.app)
        self.multiplayer_menu = MultiplayerMenu(self.app, visible=DISABLE)
        self.quit_menu = QuitMenu(self.app, visible=DISABLE)
        self.game_pause = GamePause(self.app, visible=DISABLE)

        self.prev_menu_to_render = None
        self.node = MenuHistory()
        self.menu_to_render = None

        self.init_menu()

        self.switch_menu = {
            0: self.menu_to_render,
            1: self.start_game,
            2: self.multiplayer_menu,
            3: self.menu,
            4: self.quit_menu,
            5: self.multiplayer_menu,
            6: self.menu,
            7: self.quit,
            8: self.back_to_prev_menu,
            9: self.start_game
        }

    def choose_menu(self):

        if self.menu_to_render and not callable(self.menu_to_render):
            self.menu_to_render.check_event()
            opt = self.menu_to_render.get_option()
            self.menu_to_render.set_visible(DISABLE)

            self.menu_to_render = self.switch_menu[opt]

            if not callable(self.menu_to_render):
                self.node.add(self.menu_to_render)

            self.switch_menu.update({0: self.menu_to_render})

        if self.menu_to_render and not callable(self.menu_to_render):
            self.menu_to_render.set_visible(ENABLE)

        elif self.menu_to_render and callable(self.menu_to_render):
            self.menu_to_render()

    def init_menu(self):
        self.menu_to_render = self.menu
        self.node.add(self.menu_to_render)

    def render(self):
        if self.app.menu_flag:

            if callable(self.menu_to_render) and self.app.game_start_flag:
                self.menu_to_render = self.game_pause
                self.menu_to_render.set_visible(ENABLE)
                self.node.add(self.menu_to_render)

            if self.menu_to_render and self.menu_to_render.visible:
                self.menu_to_render.update()

    def back_to_prev_menu(self):
        self.node.show_all()
        self.menu_to_render = self.node.get_prev()
        self.menu_to_render.set_visible(ENABLE)
        self.node.add(self.menu_to_render)

    def quit(self):
        pg.quit()
        sys.exit()

    def start_game(self):
        self.app.menu_flag = False
        self.app.game_start_flag = True
        self.node.clear()


class App:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.menu_flag = True
        self.game_start_flag = False

        self.menu_render = MenuRenderer(self)

    def draw(self):
        self.screen.fill('black')

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and not self.menu_flag:
                self.menu_flag = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and self.menu_flag and self.game_start_flag:
                self.menu_flag = False

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.menu_flag:
                self.menu_render.choose_menu()
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                pass

    def update(self):

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'menu app')

    def draw_menu(self):
        self.screen.fill('dark green')
        self.menu_render.render()

    def run(self):
        while True:
            self.check_events()
            if self.menu_flag:
                self.draw_menu()
            else:
                self.draw()

            self.update()


if __name__ == '__main__':
    main_app = App()
    main_app.run()
