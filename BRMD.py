import pygame

pygame.init()

W, H = 800, 600



screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('BRDM-2 Game')
pygame.display.set_icon(pygame.image.load("BRDM-2.1.bmp"))
image = pygame.image.load('Car.bmp')
new_image = pygame.transform.scale(image, (100, 100))
brdm_pose = image.get_rect(center = (W//2, H//2))

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
                y += speed
    screen.fill(WHITE)
    screen.blit(image, brdm_pose)
    pygame.display.update()
    clock.tick(60)

