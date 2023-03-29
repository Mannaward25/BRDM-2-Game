from settings import *


class Cache:
    """
    future: might be possible to store cached data in binary file using pickle or shelve module
    will try to implement that feature to shorten loading time
    """
    def __init__(self):
        self.stacked_sprite_cache = {}
        self.viewing_angle = 360 // NUM_ANGLES
        self.get_stacked_sprite_cache()

    def get_layer_array(self, attrs):
        # load sprite sheet
        sprite_sheet = pg.image.load(attrs['path']).convert_alpha()
        # scaling
        sprite_sheet = pg.transform.scale(sprite_sheet,
                                          Vec2(sprite_sheet.get_size()) * attrs['scale'])
        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()
        sprite_height = sheet_height // attrs['num_layers']

        # new sheet_height to prevent errors
        sheet_height = sprite_height * attrs['num_layers']
        # get sprites
        layer_array = []
        for y in range(0, sheet_height, sprite_height):
            sprite = sprite_sheet.subsurface((0, y, sheet_width, sprite_height))
            layer_array.append(sprite)

        return layer_array[::-1]

    def run_prerender(self, obj_name, layer_array, attrs):
        for angle in range(NUM_ANGLES):
            surf = pg.Surface(layer_array[0].get_size())
            surf = pg.transform.rotate(surf, angle * self.viewing_angle)
            sprite_surf = pg.Surface([surf.get_width(),
                                      surf.get_height() + attrs['num_layers'] * attrs['scale']])
            sprite_surf.fill('khaki')
            sprite_surf.set_colorkey('khaki')

            for idx, layer in enumerate(layer_array):
                layer = pg.transform.rotate(layer, angle * self.viewing_angle)
                sprite_surf.blit(layer, (0, idx * attrs['scale']))

            image = pg.transform.flip(sprite_surf, True, True)
            self.stacked_sprite_cache[obj_name]['rotated_sprites'][angle] = image

    def get_stacked_sprite_cache(self):
        for obj_name in STACKED_SPRITE_ASSETS:
            self.stacked_sprite_cache[obj_name] = {
                'rotated_sprites': {}
            }
            attrs = STACKED_SPRITE_ASSETS[obj_name]
            layer_array = self.get_layer_array(attrs)

            self.run_prerender(obj_name, layer_array, attrs)
