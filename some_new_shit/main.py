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


rect = RectObject(screenObj, ColorType(pl.GREEN), SizeType(800, 50), CoordType(0, 550))
rect.init()

while pl.running:
    screen.fill()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ellipse.get_physical_object().dynamic()
    rect.get_physical_object().static()
    #print(ellipse.get_physical_object().speed)
    #print(ellipse.get_physical_object().PHYS_OBJECTS_CASH)
    #print(ellipse.collide_array)

    screen.update()
    screen.set_clock()
