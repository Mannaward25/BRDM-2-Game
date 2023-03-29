from settings import *
import math


class Player(pg.sprite.Sprite):

    def __init__(self, app):
        self.game = app
        self.group = app.main_group
        super().__init__(self.group)

        size = Vec2([50, 50])
        self.image = pg.Surface(size, pg.SRCALPHA)
        pg.draw.circle(self.image, 'red', size / 2, size[0] / 2)
        self.rect = self.image.get_rect(center=CENTER)

        self.offset = Vec2(0)
        self.dx, self.dy = 0, 0

    def move(self):
        self.offset.x += self.dx
        self.offset.y += self.dy

    def control(self):
        self.dx, self.dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time

        key_state = pg.key.get_pressed()
        if key_state[pg.K_w]:
            self.dy += -speed
        if key_state[pg.K_s]:
            self.dy += speed
        if key_state[pg.K_a]:
            self.dx += -speed
        if key_state[pg.K_d]:
            self.dx += speed

    def update(self):
        self.control()
        self.move()
