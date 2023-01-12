import pygame
import random
import math
from pygame.locals import *

v1, v2 = pygame.init()
print(v1, v2, sep=' | ')

SCREEN_X = 800
SCREEN_Y = 600

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption('BRDM-2 Game')

clock = pygame.time.Clock()
FPS = 30
running = True

BLUE = pygame.Color((0, 0, 255))
GREEN = pygame.Color((0, 255, 0))
WHITE = pygame.Color((255, 255, 255))
RED = pygame.Color((255, 0, 0))
YELLOW = pygame.Color((255, 255, 0))


colors = [BLUE, GREEN, RED]


rect_x_1 = 100
rect_y_1 = 150
# rect_x_2 = 400
# rect_y_2 = 450
# rect_x_3 = 100
# rect_y_3 = 550
# rect_x_4 = 500
# rect_y_4 = 150
shift_speed_x = shift_speed_y = 8
color = GREEN
FIGURE_BANK = []


def gen_random_tuple() -> tuple:
    return random.randint(0, SCREEN_X), random.randint(0, SCREEN_Y)


def shift_position(x, y, screen_obj) -> tuple:
    global shift_speed_y
    global shift_speed_x
    global color

    if x > SCREEN_X - 100:
        shift_speed_x = -shift_speed_x
        color = random.choice(colors)
        FIGURE_BANK.append(FunnyPolygon(screen_obj, color,
                                        gen_random_tuple(), gen_random_tuple(),
                                        gen_random_tuple(), gen_random_tuple()))

    elif x <= 0:
        shift_speed_x = -shift_speed_x
        color = random.choice(colors)
        FIGURE_BANK.append(FunnyPolygon(screen_obj, color,
                                        gen_random_tuple(), gen_random_tuple(),
                                        gen_random_tuple(), gen_random_tuple()))

    if y > SCREEN_Y - 50:
        shift_speed_y = -shift_speed_y
        color = random.choice(colors)
        #shift_speed_x = -shift_speed_x
        color = random.choice(colors)
        FIGURE_BANK.append(FunnyPolygon(screen_obj, color,
                                        gen_random_tuple(), gen_random_tuple(),
                                        gen_random_tuple(), gen_random_tuple()))
    elif y <= 0:
        shift_speed_y = -shift_speed_y
        color = random.choice(colors)
        #shift_speed_x = -shift_speed_x
        color = random.choice(colors)
        FIGURE_BANK.append(FunnyPolygon(screen_obj, color,
                                        gen_random_tuple(), gen_random_tuple(),
                                        gen_random_tuple(), gen_random_tuple()))

    x += shift_speed_x
    y += shift_speed_y

    return x, y


class FunnyPolygon:
    def __init__(self, surface, obj_color, top_left=(50, 100),
                 top_right=(100, 100), bottom_right=(100, 150), bottom_left=(50, 150), width=2):
        self.polygon_top_left = self._left_top = top_left
        self.polygon_top_right = top_right
        self.polygon_bottom_right = self._right_bottom = bottom_right
        self.polygon_bottom_left = bottom_left
        self.polygon_coord_print()
        self.surface = surface
        self.obj_color = obj_color
        self.obj_width = width
        self.polygon = self.draw(surface, obj_color, ((0, 0), (0, 0), (0, 0), (0, 0)), width)
        print('ok')

        self.center_coord = self.get_polygon_center(self._left_top, self._right_bottom)
        self.r_distance = self.get_distance(self.coord_substract(self._left_top,
                                                                 self.center_coord))  # float var

    def get_polygon_center(self, t1, t2) -> tuple:
        tmp = ((t1[0] + t2[0]) / 2, (t1[1] + t2[1]) / 2)
        tmp = tuple(map(int, tmp))
        return tmp

    def coord_substract(self, t1, t2) -> tuple:
        #  tmp = (abs(t1[0] - t2[0]), abs(t1[1] - t2[1]))
        tmp = (t1[0] - t2[0]), (t1[1] - t2[1])
        tmp = tuple(map(int, tmp))
        return tmp

    def coord_add(self, t1, t2) -> tuple:
        tmp = (t1[0] + t2[0]), (t1[1] + t2[1])
        return tmp

    def get_distance(self, dist_coord: tuple) -> float:
        res = math.sqrt(math.pow(dist_coord[0], 2) + math.pow(dist_coord[1], 2))
        print(res)
        return res

    @staticmethod
    def calc_coord(r: float, degree: int) -> tuple:  # r - radius
        rad = math.radians(degree)  # radian
        sinus = math.sin(rad)
        cosin = math.cos(rad)
        y_coord = int(sinus * r)
        x_coord = int(cosin * r)
        print(x_coord, y_coord)
        return x_coord, y_coord

    def polygon_coord_print(self):
        print('polygon_top_left = ', self.polygon_top_left,
              'polygon_top_right = ', self.polygon_top_right,
              'polygon_bottom_left = ', self.polygon_bottom_left,
              'polygon_bottom_right = ', self.polygon_bottom_right)

    def draw(self, surface, obj_color, rect, width):
        return pygame.draw.polygon(surface, obj_color, rect, width)

    def change_color(self, obj_color):
        self.obj_color = obj_color

    def move_figure(self):
        self.polygon_bottom_right = shift_position(*self.polygon_bottom_right)
        self.polygon_bottom_left = shift_position(*self.polygon_bottom_left)
        self.polygon_top_right = shift_position(*self.polygon_top_right)
        self.polygon_top_left = shift_position(*self.polygon_top_left)

        self.draw(self.surface, self.obj_color, (self.polygon_top_left, self.polygon_top_right,
                                                 self.polygon_bottom_right, self.polygon_bottom_left),
                  self.obj_width)

    def rotate_polygon(self, ang_degree):
        a_deg = ang_degree

        print(self.center_coord)

        self.polygon_top_right = self.coord_add(self.center_coord,
                                                self.calc_coord(self.r_distance, a_deg))
        self.polygon_top_left = self.coord_add(self.center_coord,
                                               self.calc_coord(self.r_distance, a_deg + 90))
        self.polygon_bottom_left = self.coord_add(self.center_coord,
                                                  self.calc_coord(self.r_distance, a_deg + 180))
        self.polygon_bottom_right = self.coord_add(self.center_coord,
                                                   self.calc_coord(self.r_distance, a_deg + 270))

        self.draw(self.surface, self.obj_color, (self.polygon_top_left, self.polygon_top_right,
                                                 self.polygon_bottom_right, self.polygon_bottom_left),
                  self.obj_width)


deg = 45


while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rect_x_1, rect_y_1 = shift_position(rect_x_1, rect_y_1, screen)
    # rect_x_2, rect_y_2 = shift_position(rect_x_2, rect_y_2, screen)
    # rect_x_3, rect_y_3 = shift_position(rect_x_3, rect_y_3, screen)
    # rect_x_4, rect_y_4 = shift_position(rect_x_4, rect_y_4, screen)
    # pol = pygame.draw.polygon(screen, color, (polygon_top_left, polygon_top_right,
    #                                           polygon_bottom_right, polygon_bottom_left), 2)
    for obj in FIGURE_BANK:
        obj.change_color(color)

        obj.rotate_polygon(deg)

    pygame.draw.rect(screen, color, (rect_x_1, rect_y_1, 100, 50))
    # pygame.draw.rect(screen, color, (rect_x_2, rect_y_2, 100, 50))
    # pygame.draw.rect(screen, color, (rect_x_3, rect_y_3, 100, 50))
    # pygame.draw.rect(screen, color, (rect_x_4, rect_y_4, 100, 50))
    pygame.display.update()
    clock.tick(FPS)
    deg += 1



