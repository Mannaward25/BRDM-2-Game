import math
import ctypes
USER32 = ctypes.windll.user32
SCREEN_W, SCREEN_H = USER32.GetSystemMetrics(0), USER32.GetSystemMetrics(1)
print(SCREEN_W, SCREEN_H)

#  BLOCK SIZE
BLOCK_SIZE = 100  #  100 for (1600, 900)  50 for (1200, 600)  # + 1920 1080
WEAPON_SCALE = 0.3  # 0.4 for (1600, 900) 0.3 for (1200, 600)
PLAYER_SIZE_SCALE = 80

#  window settings
RES = WIDTH, HEIGHT = (SCREEN_W, SCREEN_H)  # (1600, 900) (1200, 600)  # +
FPS = 120  # +

#  game settings
PLAYER_POS = 1.5, 2.8  # +
PLAYER_ANGLE = 0  # +
PLAYER_SPEED = 0.0035  # +
PLAYER_ROT_SPEED = 0.002  # rotation speed  # +
PLAYER_MAX_HEALTH = 100
PLAYER_HEIGHT = 0.5  # for floor raycasting
HALF_WIDTH = WIDTH // 2  # +
HALF_HEIGHT = HEIGHT // 2  # +

# Raycasting settings
FOV = math.pi / 3  # +
DEG_FOV = 60
HALF_DEG_FOV = DEG_FOV // 2
HALF_FOV = FOV / 2  # +
NUM_RAYS = WIDTH // 2  # +
HALF_NUM_RAYS = NUM_RAYS // 2  # +
DELTA_ANGLE = FOV / NUM_RAYS  # +
MAX_DEPTH = 20  # +

# Vector raycasting

#  colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
DARK_GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)
BLUE = (0, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 255)
WHITE = (255, 255, 255)
FLOOR_COLOR = (35, 35, 35)  # 255, 204, 102, |  115, 140, 121 |  35, 35, 35

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)  # +
SCALE = WIDTH // NUM_RAYS  # +

# texture settings

TEXTURE_SIZE = 256  # +
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2  # +

# mouse control

MOUSE_SENSITIVITY = 0.004
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 200
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# Background Fire implementation
STEP_BETWEEN_COLORS = 4
FLAME_COLORS = [
    BLACK,
    RED,
    ORANGE,
    YELLOW,
    WHITE
]

FIRE_REPS = 4
PIXEL_SIZE = 6
FIRE_HEIGHT = HEIGHT // PIXEL_SIZE
FIRE_WIDTH = WIDTH // (PIXEL_SIZE * FIRE_REPS)

# floor ray_cast
FLOOR_TEXTURE = 25
HOR_FLOOR_RAYS = 120
VERT_FLOOR_RAYS = 200
VERT_FLOOR_RAYS_HALF = VERT_FLOOR_RAYS // 2
DELTA_FLOOR_HOR = FOV / 120

# MODE7

FOCAL_LEN = 250
MODE_SEVEN_SCALE = 100

# NETWORK SETTINGS

PORT = 6666
MAX_PLAYERS = 3
DATA_RECV_CHUNK = 2048
LOCAL_SERVER_IP = '25.66.120.65'  # 192.168.1.110, 192.168.1.129 25.66.120.65

PLAYER_MODEL_CONSTANT = 22.5  # degrees
HALF_PI = math.pi / 2
H_PI_DEG = math.degrees(HALF_PI)


# directions
EAST = (1, 0)
WEST = (-1, 0)
NORTH = (0, -1)
SOUTH = (0, 1)
NE = (1, -1)
NW = (-1, -1)
SE = (1, 1)
SW = (-1, 1)

# messages
CLOSE = 'close'

# menu settings

FONT_SIZE = 24
INIT_RECT = (0, 0, 0, 0)
ENABLE = True
DISABLE = False
DEFAULT_BTN_SIZE = (260, 40)

# menu buttons
SINGLE_GAME = 'Single Game'
MULTIPLAYER = 'Multiplayer'
SETTINGS = 'Settings'
QUIT = 'Quit'
BACK = 'Back'
CONNECT = 'Connect'
YES = 'Yes'
CONTINUE = 'Continue'
MAIN = 'Back to main'
END = 'Go to main menu'
SWITCH_SOUND = 'Switch sound'
