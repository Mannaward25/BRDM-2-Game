import pygame as pg

Vec2 = pg.math.Vector2

RES = WIDTH, HEIGHT = 1600, 900
CENTER = WIDTH // 2, HEIGHT // 2
FPS = 120

NUM_ANGLES = 90
PLAYER_SPEED = 0.4
VIEWING_ANGLE = 360 // NUM_ANGLES


# colors
BG_COLOR = (20, 30, 46)  # (20, 30, 46)

# stacked sprite settings

STACKED_SPRITE_ASSETS = {
    'van': {
        'path': 'resources/sprite/stacked_sprite/van.png',
        'num_layers': 20,
        'scale': 8
           },
    'brdm': {
        'path': 'resources/sprite/stacked_sprite/brdm.png',
        'num_layers': 40,
        'scale': 4
            },
    'tank': {
        'path': 'resources/sprite/stacked_sprite/tank.png',
        'num_layers': 17,
        'scale': 13
             }

}
