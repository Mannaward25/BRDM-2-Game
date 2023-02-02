from sprite_object import *
from npc import *


class ObjectHandler:

    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        # sprite map
        add_sprite(SpriteObject(game))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'grass.png', pos=(2, 1.6)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'grass.png', pos=(2.5, 4.8)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'grass.png', pos=(3, 4)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'grass.png', pos=(2.2, 1.6)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'grass.png', pos=(2, 4)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'grass.png', pos=(7, 4)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'grass.png', pos=(12.5, 1.5)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'grass.png', pos=(13, 6)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'grass.png', pos=(14.8, 7)))
        #add_sprite(SpriteObject(game, path=self.static_sprite_path + 'crate.png', pos=(12.5, 3.5),
        #                        scale=0.6, shift=0.5))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(5.2, 7.7)))

        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.9, 1.55), scale=0.6))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14, 1.2)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(13, 1.2)))

        # npc map
        add_npc(NPC(game))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_npc(self, npc):
        self.npc_list.append(npc)
