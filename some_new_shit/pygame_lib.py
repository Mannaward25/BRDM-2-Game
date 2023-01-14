import pygame
import random

FPS = 30
SCREEN_X = 800
SCREEN_Y = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

running = True


class InitWindow:
    def __init__(self, title: str = "pygame", coord: tuple = (SCREEN_X, SCREEN_Y)):
        self._screen = pygame.display.set_mode(coord)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    def __repr__(self):
        return f'{self._screen.__class__}'

    def __str__(self):
        return f'{self._screen}'

    def get_obj(self):
        return self._screen

    def set_clock(self, tick=FPS):
        self.clock.tick(tick)

    def fill(self, color=WHITE):
        self._screen.fill(color)

    def blit(self, surface, rect, area=None, flags=None):
        self._screen.blit(surface, rect)

    def set_icon(self):
        pass

    @staticmethod
    def update():
        pygame.display.update()


class PolygonModel:
    def __init__(self):
        pass


class TextModel:
    def __init__(self, parent_surface, name, size=16):
        pygame.font.init()

        self.parent_surf = parent_surface
        self.center = 0, 0
        self.font_obj = pygame.font.Font(name, size)
        self.text_rect = 0
        self.text = "none"

    def render(self, text=None, text_color=BLACK, background_color=WHITE, center=(SCREEN_X / 2, SCREEN_Y / 2)):

        if text:
            self.text = text
        else:
            text = self.text

        antialiasing = True
        font_surface = self.font_obj.render(text, antialiasing, text_color, background_color)
        font_rect = font_surface.get_rect()
        font_rect.center = center
        self.parent_surf.blit(font_surface, font_rect)
        self.text_rect = font_rect

    def get_rect(self):
        return self.text_rect


def gen_random_color() -> tuple:
    gen_color = tuple(random.randint(0, 255) for _ in range(3))
    return gen_color



