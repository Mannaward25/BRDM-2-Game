import pygame
import pygame_lib as pl
from pygame.locals import *

screen = pl.InitWindow()

screen.fill()  # WHITE by default

while pl.running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pl.running = False
        else:
            print(event)

    screen.update()
    screen.set_clock()  # 30 by default