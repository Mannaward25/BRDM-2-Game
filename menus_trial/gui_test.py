import pygame as pg
import pygame_gui as pgg
import sys
import re
from settings import *


class Menu:

    def __init__(self, app):
        self.manager = pgg.UIManager(RES)
        self.app = app
        self.x, self.y = self.centered_position()


    @staticmethod
    def get_rect(pos, size=DEFAULT_BTN_SIZE):
        return pg.Rect(pos, size)

    @staticmethod
    def centered_position(size=()):
        def_pos_x, def_pos_y = 0, 0
        if size:
            def_el_size = size[0]
            def_pos_x = (WIDTH // 2) - (def_el_size // 2)
            def_pos_y = (HEIGHT // 2) - (def_el_size // 2)
        else:
            def_el_size = DEFAULT_BTN_SIZE[0]
            def_pos_x = (WIDTH // 2) - (def_el_size // 2)
            def_pos_y = (HEIGHT // 2) - (def_el_size // 2)
        return def_pos_x, def_pos_y

    def process(self, event):
        self.manager.process_events(event)

    def draw(self):
        self.manager.draw_ui(self.app.screen)

    def update(self, delta_time):
        self.manager.update(delta_time)


class MainMenu(Menu):

    def __init__(self, app):
        super().__init__(app)

        self.single_play_btn = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y)),
                                                     text=SINGLE_GAME,
                                                     manager=self.manager)
        self.multiplayer_btn = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y + 50)),
                                                     text=MULTIPLAYER,
                                                     manager=self.manager)
        self.settings = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y + 100)),
                                              text=SETTINGS,
                                              manager=self.manager)
        self.test_btn = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y + 150)),
                                              text=TEST,
                                              manager=self.manager)
        self.quit_btn = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y + 200)),
                                              text=QUIT,
                                              manager=self.manager)

    def test(self):
        return self.single_play_btn


class MultiplayerMenu(Menu):

    def __init__(self, app):
        super().__init__(app)
        self.ip_input = pgg.elements.UITextEntryLine(relative_rect=self.get_rect((self.x, self.y)),
                                                     manager=self.manager)
        self.connect_btn = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y + 50)),
                                                 text=CONNECT,
                                                 manager=self.manager)
        self.back_btn = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y + 100)),
                                              text=BACK,
                                              manager=self.manager)
        self.label = pgg.elements.UILabel(relative_rect=self.get_rect((self.x, self.y + 150)),
                                          text='',
                                          manager=self.manager)

    def get_input_object(self):
        return self.ip_input

    def get_label(self):
        return self.label


class QuitMenu(Menu):

    def __init__(self, app):
        super().__init__(app)
        self.label = pgg.elements.UILabel(relative_rect=self.get_rect((self.x, self.y)),
                                          text='Do you really want to quit?',
                                          manager=self.manager)
        self.yes_btn = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y + 50)),
                                             text=YES,
                                             manager=self.manager)
        self.no_btn = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y + 100)),
                                            text=BACK,
                                            manager=self.manager)


class TestMenu(Menu):

    def __init__(self, app):
        super().__init__(app)
        x, y = self.centered_position((460, 240))
        self.text_field = pgg.elements.UITextEntryBox(relative_rect=self.get_rect((x, y), (460, 240)),
                                                      initial_text='',
                                                      manager=self.manager)
        self.text_field.disable()
        self.back_btn = pgg.elements.UIButton(relative_rect=self.get_rect((self.x, self.y + 290)),
                                              text=BACK,
                                              manager=self.manager)


class MenuManager:

    def __init__(self, app):
        self.app = app
        self.main_menu = MainMenu(app)

        self.multiplayer_menu = MultiplayerMenu(app)
        self.input_object = self.multiplayer_menu.get_input_object()
        self.label_object = self.multiplayer_menu.get_label()

        self.quit_menu = QuitMenu(app)
        self.test_menu = TestMenu(app)

        self.history = MenuHistory()

        self.menu_options = {
            SINGLE_GAME: self.start_game,
            MULTIPLAYER: self.multiplayer_menu,
            BACK: self.back_to_prev_menu,
            QUIT: self.quit_menu,
            YES: self.quit_game,
            CONNECT: self.get_ip_address,
            TEST: self.test_menu
        }

        self.context_menu = self.init_menu()

    def init_menu(self):
        self.history.add(self.main_menu)
        return self.main_menu

    def context_switcher(self, context):
        if isinstance(context, Menu):
            self.history.add(context)
            self.context_menu = context

        elif callable(context):
            context()

    def menu_events(self, event):
        if event.type == pgg.UI_BUTTON_PRESSED:
            print(event.ui_element.text)
            context = self.menu_options.get(event.ui_element.text, False)
            if context:
                self.context_switcher(context)

        self.context_menu.process(event)

    def draw(self):
        self.context_menu.draw()

    def update(self, delta_time):
        self.context_menu.update(delta_time)

    def back_to_prev_menu(self):
        self.context_menu = self.history.get_prev()
        self.history.add(self.context_menu)

    def quit_game(self):
        pg.quit()
        sys.exit()

    def get_ip_address(self):
        pattern = r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$'
        text = self.input_object.get_text()
        self.input_object.set_text('')
        res = re.search(pattern, text)
        if res:
            self.label_object.set_text(f'success! {res.group()}')
        else:
            self.label_object.set_text('invalid ip, try input again!')

    def start_game(self):
        pass


class ContextNode:

    def __init__(self, menu, node=None):
        self.data = menu
        self.prev = node


class MenuHistory:

    def __init__(self):
        self.head = None
        self.cur = None
        self.total_nodes = 0

    def add(self, data):
        if not self.head:
            self.head = ContextNode(data)
            self.cur = self.head
        else:
            prev = self.cur
            self.cur = ContextNode(data, prev)
        self.total_nodes += 1

        self.auto_delete()

    def get_prev(self):
        return self.cur.prev.data

    def auto_delete(self):
        if self.total_nodes > 4:
            self.head = self.cur.prev
            self.head.prev = None
            self.total_nodes = 2

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


class App:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.background = pg.Surface(RES)
        self.menu_manager = MenuManager(self)

        self.menu_flag = True
        self.game_start_flag = False

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
                pass
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                pass

            self.menu_manager.menu_events(event)

    def update(self):
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)

        self.menu_manager.update(self.delta_time)
        pg.display.set_caption(f'menu app')

    def draw_menu(self):
        self.background.fill('dark green')
        self.screen.blit(self.background, (0, 0))
        self.menu_manager.draw()

    def run(self):
        while True:
            self.check_events()
            if self.menu_flag:
                self.update()
                self.draw_menu()
            else:
                self.draw()

                self.update()


if __name__ == '__main__':
    main_app = App()
    main_app.run()
