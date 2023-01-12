import pygame

pygame.init()


screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('BRDM-2 Game')
pygame.display.set_icon(pygame.image.load("BRDM-2.1.bmp"))
image = pygame.image.load('Car.bmp')
new_image = pygame.transform.scale(image, (100, 100))
brdm_pose = image.get_rect(center = (10, 10))

clock = pygame.time.Clock()
FPS = 60
running = True

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

#передвижение БРДМ


# Полезности
# pygame.draw.rect(screen, WHITE, (10,10, 50, 100), 2)
# pygame.draw.line(screen, BLUE, (10, 200), (350, 50))
# pygame.draw.aaline(screen, GREEN, (200, 40), (350, 50))
# pygame.draw.polygon(screen,GREEN, [[150, 210], [180,250],[90, 290],[30,230]], 1)
# pygame.display.update()

x = 200
speed = 5

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
         x += 10
    if keys[pygame.K_a]:
         x -= 10
    screen.fill(WHITE)
    screen.blit(image, (x, 10))
    pygame.display.update()
    clock.tick(30)

