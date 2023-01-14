import pygame
import sys
from pygame.locals import *
import pygame_lib as pl
from physcore import *

screen = pl.InitWindow()
screenObj = screen.get_obj()


screen.fill()
#obj = pygame.draw.ellipse(screenObj, pl.BLACK, (100, 50, 30, 30))

ellipse = EllipseObject(screenObj, ColorType(pl.RED), SizeType(50, 50), CoordType(100, 200))
ellipse.init()
#ellipse.physical_object.speed

x = 0
y = 0
while pl.running:
    screen.fill()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    x += 1
    y += 1
    ellipse.redraw(CoordType(100 + x, 200 + y))

    screen.update()

    screen.set_clock()