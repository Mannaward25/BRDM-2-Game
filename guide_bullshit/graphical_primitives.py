import pygame
import random
from pygame.locals import *
import pygame_lib as pg



def gen_random_color() -> tuple:
    gen_color = tuple(random.randint(0, 255) for _ in range(3))
    return gen_color


pygame.init()

SCREEN_X = 800
SCREEN_Y = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RAND_COLOR = gen_random_color()


screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption("test")
clock = pygame.time.Clock()
FPS = 30
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    pygame.draw.polygon(screen, RAND_COLOR, ((100, 50), (200, 50), (250, 100), (200, 150), (100, 150)))

    pixObj = pygame.pixelarray.PixelArray(screen)
    pixObj[480][380] = BLACK
    # pixObj[482][382] = BLACK
    # pixObj[484][384] = BLACK
    # pixObj[486][386] = BLACK
    # pixObj[488][388] = BLACK
    del pixObj

    pygame.display.update()
    clock.tick(FPS)


