import pygame
import pygame_lib as pl
from pygame.locals import *

screen = pl.InitWindow()

mouse_x = 0
mouse_y = 0
clicked = False

screen.fill()  # WHITE by default
fontObj = pl.TextModel(screen, 'USSR STENCIL WEBFONT.ttf', 32)
fontObj.render("Hello world!")

while pl.running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pl.running = False
        elif event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            clicked = True

    if fontObj.get_rect().collidepoint(mouse_x, mouse_y) and clicked:
        print("collide!", f" position x: {mouse_x}; y: {mouse_y};")
        fontObj.render(text_color=pl.gen_random_color())
        clicked = False

    screen.update()
    screen.set_clock()  # 30 by default
