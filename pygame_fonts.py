import pygame
import pygame_lib as pl

screen = pl.InitWindow()

while pl.running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pl.running = False

    screen.fill()  # WHITE by default

    pygame.font.init()
    fontObj = pygame.font.Font('USSR STENCIL WEBFONT.ttf', 32)
    textSurfaceObj = fontObj.render('Hello wordl!', True, pl.BLACK, pl.WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 150)

    screen.blit(textSurfaceObj, textRectObj)

    screen.update()
    screen.set_clock()  # 30 by default
