import pygame
from pygame.locals import *

v1, v2 = pygame.init()
print(v1, v2, sep=' | ')


screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('BRDM-2 Game')
pygame.display.set_icon(pygame.image.load("BRDM-2.1.bmp"))


image = pygame.image.load('Car.bmp')
new_image = pygame.transform.scale(image, (200, 200))

brdm_pose = image.get_rect(center=(10, 10))

clock = pygame.time.Clock()
FPS = 30
running = True

#WHITE = (255, 255, 255)
BLUE = pygame.Color((0, 0, 255))
GREEN = pygame.Color((0, 255, 0))

WHITE = pygame.Color((255, 255, 255))

#передвижение БРДМ


# Полезности
# pygame.draw.rect(screen, WHITE, (10,10, 50, 100), 2)
# pygame.draw.line(screen, BLUE, (10, 200), (350, 50))
# pygame.draw.aaline(screen, GREEN, (200, 40), (350, 50))
# pygame.draw.polygon(screen,GREEN, [[150, 210], [180,250],[90, 290],[30,230]], 1)
# pygame.display.update()

x_coord = 100
y_coord = 150
speed = 10
FALL_DOWN = 10

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #     elif event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT:
    #             x -= speed
    #         elif event.key == pygame.K_RIGHT:
    #             y += speed

    if keys[pygame.K_d]:
        x_coord += speed
    if keys[pygame.K_a]:
        x_coord -= speed
    if keys[pygame.K_SPACE]:
        while y_coord > 350:
            y_coord -= 3
            screen.blit(image, (x_coord, y_coord))
            pygame.display.update()
    else:
        if y_coord < 450:
            y_coord += FALL_DOWN

    if y_coord < 480:
        y_coord += FALL_DOWN



    screen.fill(WHITE)
    screen.blit(image, (x_coord, y_coord))
    pygame.display.update()
    clock.tick(FPS)

