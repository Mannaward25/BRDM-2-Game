import pygame

pygame.init()
screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption('BRDM-2 Game')
pygame.display.set_icon(pygame.image.load("BRDM-2.1.bmp"))
clock = pygame.time.Clock()
running = True

pygame.draw.rect(screen,(255,255,255), (10,10, 50, 100))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)

