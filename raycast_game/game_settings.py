import math

#  window settings
RES = WIDTH, HEIGHT = (1600, 900)  # (1600, 900) (1200, 600)
FPS = 120

#  game settings
PLAYER_POS = 1.5, 5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.032
PLAYER_ROT_SPEED = 0.016  # rotation speed

# Raycasting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

#  colors
BLACK = (0, 0, 0)
DARK_GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 255)

#  BLOCK SIZE
BLOCK_SIZE = 100  #  100 for (1600, 900)  50 for (1200, 600)

