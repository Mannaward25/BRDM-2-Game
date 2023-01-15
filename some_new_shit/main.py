import pygame
import sys
from pygame.locals import *
import pygame_lib as pl
from physcore import *
import random

screen = pl.InitWindow()
screenObj = screen.get_obj()


screen.fill()
#obj = pygame.draw.ellipse(screenObj, pl.BLACK, (100, 50, 30, 30))

ellipse = EllipseObject(screenObj, ColorType(pl.RED), SizeType(50, 50), CoordType(100, 200))
ellipse.init()


rect = RectObject(screenObj, ColorType(pl.GREEN), SizeType(800, 50), CoordType(0, 550))
rect.init()

# rect_2 = RectObject(screenObj, ColorType(pl.GREEN), SizeType(50, 50), CoordType(400, 300))
# rect_2.init()
#
# rect_3 = RectObject(screenObj, ColorType(pl.BLACK), SizeType(50, 50), CoordType(200, 100))
# rect_3.init()
#
# rect_4 = RectObject(screenObj, ColorType(pl.CYAN), SizeType(80, 80), CoordType(500, 100))
# rect_4.init()
#
# rect_5 = RectObject(screenObj, ColorType(pl.YELLOW), SizeType(80, 50), CoordType(600, 100))
# rect_5.init()

while pl.running:
    screen.fill()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ellipse.get_physical_object().dynamic()
    rect.get_physical_object().static()
    # rect_2.get_physical_object().dynamic()
    # rect_3.get_physical_object().dynamic()
    # rect_4.get_physical_object().dynamic()
    # rect_5.get_physical_object().dynamic()
    #print(ellipse.get_physical_object().speed)
    #print(ellipse.get_physical_object().PHYS_OBJECTS_CASH)
    #print(ellipse.collide_array)

    screen.update()
    screen.set_clock()
