import pygame

pygame.init()

W = 800
H = 600


screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('BRDM-2 Game')
pygame.display.set_icon(pygame.image.load("BRDM-2.1.bmp"))
image = pygame.image.load('Car.bmp').convert_alpha()
new_image = pygame.transform.scale(image, (10, 10))
clock = pygame.time.Clock()
FPS = 60
running = True

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Полезности
# pygame.draw.rect(screen, WHITE, (10,10, 50, 100), 2)
# pygame.draw.line(screen, BLUE, (10, 200), (350, 50))
# pygame.draw.aaline(screen, GREEN, (200, 40), (350, 50))
# pygame.draw.polygon(screen,GREEN, [[150, 210], [180,250],[90, 290],[30,230]], 1)
# pygame.display.update()

x = W // 2
y = H // 2
speed = 5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= speed
            elif event.key == pygame.K_RIGHT:
                x += speed
    screen.fill(WHITE)
    screen.blit(image, (100, 100))
    pygame.display.update()
    clock.tick(60)

