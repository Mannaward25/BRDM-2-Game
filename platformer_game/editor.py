import pygame as pg
from pygame.math import Vector2 as Vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
import sys
from settings import *


class Editor:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        # navigation
        self.origin = Vector()
        self.pan_active = False
        self.pan_offset = Vector()  # vector between origin and mouse pos

    # input
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT \
                    or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            self.pan_input(event)

    def pan_input(self, event):
        """
        pygame.mouse.get_pressed() -> tuple
        mouse buttons (0,1,2) 0 for left btn, 1 for middle btn and 2 for right btn"""
        # middle mouse button pressed \ released
        if event.type == pg.MOUSEBUTTONDOWN and mouse_buttons()[1]:  #
            self.pan_active = True
            self.pan_offset = Vector(self.get_mouse_pos()) - self.origin
        if not mouse_buttons()[1]:
            self.pan_active = False

        # mouse wheel
        """
        event.y allow to get info about wheel moving. When wheel moves up we get event.y = 1
            if wheel goes down we get event.y = -1
        """
        if event.type == pg.MOUSEWHEEL:
            if pg.key.get_pressed()[pg.K_LCTRL]:
                self.origin.y -= event.y * SHIFT_X_MULTIPLY
            else:
                self.origin.x -= event.y * SHIFT_X_MULTIPLY

        # panning updated
        if self.pan_active:
            self.origin = Vector(self.get_mouse_pos()) - self.pan_offset

    def update(self, dt):
        self.event_loop()

    # drawing tiles
    def draw_tile_lines(self):
        columns = WIDTH // TILE_SIZE + 1
        rows = HEIGHT // TILE_SIZE + 1

        """
        author implementation
        
        offset_vector = Vector(
            x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE
            )
        
        for col in range(columns):
            x = offset_vector.x + col * TILE_SIZE
            pg.draw.line(self.game.screen, BLACK, (x, 0), (x, HEIGHT))
        """

        offset_vector = Vector(
            x=self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y=self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE
        )

        # my way also working but less elegant
        # columns += abs((WIDTH - (WIDTH + int(self.origin.x))) // TILE_SIZE)
        # rows += abs((HEIGHT - (HEIGHT + int(self.origin.y))) // TILE_SIZE)

        for col in range(columns):
            x = offset_vector.x + col * TILE_SIZE
            pg.draw.line(self.game.screen, BLACK, (x, 0), (x, HEIGHT))
            # # my way also working but less elegant
            # x = self.origin.x - col * TILE_SIZE
            # pg.draw.line(self.game.screen, BLACK, (x, 0), (x, HEIGHT))

        for row in range(rows):
            y = offset_vector.y + row * TILE_SIZE
            pg.draw.line(self.game.screen, BLACK, (0, y), (WIDTH, y))
            # # my way also working but less elegant
            # y = self.origin.y - row * TILE_SIZE
            # pg.draw.line(self.game.screen, BLACK, (0, y), (WIDTH, y))

    def draw(self):
        self.game.screen.fill('white')
        self.draw_tile_lines()
        pg.draw.circle(self.game.screen, 'red', self.origin, 10)  # origin is a center

    @staticmethod
    def get_mouse_pos():
        return pg.mouse.get_pos()
