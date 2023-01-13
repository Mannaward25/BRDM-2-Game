import pygame
import pygame_lib as pl
from pygame.locals import *

screen = pl.InitWindow()
screen.fill()  # WHITE by default
screenObj = screen.get_obj()

ball_x = 200
ball_y = 100
ball_w = ball_h = ball_size = 50
ball = pygame.draw.ellipse(screenObj, pl.BLACK, (ball_x, ball_y, ball_size, ball_size))

speed = 0.01


def falling_obj(y, spd):
    y += spd
    return y


while pl.running:
    screen.fill()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pl.running = False

    ball_y = falling_obj(ball_y, speed)
    pygame.draw.ellipse(screenObj, pl.BLACK, (ball_x, ball_y, ball_size, ball_size))

    screen.update()
    screen.set_clock()  # 30 by default

    if ball_y < pl.SCREEN_Y - 50:
        speed += 0.1 * 10
    elif ball_y >= pl.SCREEN_Y - 50:
        speed = -speed * 0.8
