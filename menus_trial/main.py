import pygame as pg
import sys
from settings import *


class Button:

    def __init__(self, parent, text, pos=(0, 0), size=(260, 40), center=True):
        self.menu = parent
        self.font = parent.font
        self.text = text

        self.pos = pos
        self.relative_position()
        self.size = size
        self.center = center

        self.btn: pg.Rect = pg.Rect(pos, size)

    def get_size(self):
        return self.size

    def get_pos(self):
        return self.pos

    def move(self, x, y):
        self.pos = (x, y)

    def check_collision(self):
        mouse_pos = pg.mouse.get_pos()
        if self.btn.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            print(f'pressed button {self.text}')

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
        self.check_collision()


class Menu:

    def __init__(self, app):
        self.app = app
        self.screen = self.app.screen
        self.font = pg.font.Font('freesansbold.ttf', FONT_SIZE)

        self.menu_width = 500
        self.menu_height = 500
        self.menu_pos = self.calc_sizes()
        self.menu_frame = pg.rect.Rect(INIT_RECT)

        self.menu_btn: Button = Button(self, 'Play single', pos=(100, 100))
        self.multiplayer_btn: Button = Button(self, 'Multiplayer', pos=(100, 150))
        self.settings_btn: Button = Button(self, 'Settings', pos=(100, 200))

    def get_size(self):
        return self.menu_width, self.menu_height

    def get_pos(self):
        return self.menu_pos

    def calc_sizes(self):
        margin_hor = (WIDTH - self.menu_width) // 2
        margin_vert = (HEIGHT - self.menu_height) // 2
        self.menu_pos = margin_hor, margin_vert
        return margin_hor, margin_vert

    def draw(self):
        marg_x, marg_y = self.menu_pos
        pg.draw.rect(self.screen, 'black', (marg_x, marg_y, self.menu_width, self.menu_height), width=2)

    def update(self):
        self.draw()
        self.menu_btn.update()
        self.multiplayer_btn.update()
        self.settings_btn.update()


class App:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.menu = Menu(self)

    def draw(self):
        self.screen.fill('dark green')

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def update(self):
        self.menu.update()

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
