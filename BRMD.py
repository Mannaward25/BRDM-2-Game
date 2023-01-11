import pygame

pygame.init()
screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption('BRDM-2 Game')
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(30)
print ("caca")

