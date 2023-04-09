from settings import *
import os
import io
import pickle


class Cache:
    """
    future: might be possible to store cached data in binary file using pickle or shelve module
    will try to implement that feature to shorten loading time
    """
    def __init__(self):
        self.stacked_sprite_cache = {}
        self.viewing_angle = VIEWING_ANGLE
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
                #pg.image.save(layer, f'resources/cached_sprites/{obj_name}_{angle}_{idx}.png')
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


class ByteStorage:
    def __init__(self):
        self.storage = dict()
        self.path = 'resources/cached_sprites/'
        self.load_assets(self.path)

    def get_binary_data(self, path):
        data: bytes = b''
        with open(path, 'rb') as f:
            data = f.read()

        return data

    def load_assets(self, path):
        for file in os.listdir(path):
            obj_name, angle, idx = file[:-4].split('_')
            full_path = os.path.join(path, file)

            data = self.get_binary_data(full_path)

            if obj_name not in self.storage:
                self.storage[obj_name] = {}
                if angle not in self.storage[obj_name]:
                    self.storage[obj_name][angle] = {}
                    self.storage[obj_name][angle][idx] = data
                else:
                    self.storage[obj_name][angle][idx] = data
            else:
                if angle not in self.storage[obj_name]:
                    self.storage[obj_name][angle] = {}
                    self.storage[obj_name][angle][idx] = data
                else:
                    self.storage[obj_name][angle][idx] = data

    def show_storage(self):
        for key, value in self.storage.items():
            print(key, value)

    def get_full_path(self):
        path = os.path.join(self.path, 'game_db')
        return path

    def save_database(self):
        path = self.get_full_path()
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def get_storage_data(self) -> dict:
        return self.storage


class PreloadedSprites:
    def __init__(self):
        self.stacked_sprite_cache = {}
        self.path = 'resources/cached_sprites/game_db'
        self.loaded_data: ByteStorage = None
        self.open_db(self.path)
        self.compile_sprites()

    def open_db(self, path):
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.loaded_data = data

    def byte_image_extraction(self, byte_data) -> pg.Surface:
        image: pg.Surface = None
        with io.BytesIO(byte_data) as binary_image:
            #binary_image = file.read()
            image = pg.image.load(binary_image)
        return image

    def get_stacked_sprite_cache(self, obj_names):
        for obj_name in obj_names:
            self.stacked_sprite_cache[obj_name] = {
                'rotated_sprites': {}
            }

    def compile_sprites(self):
        storage = self.loaded_data.get_storage_data()
        obj_names = list(storage.keys())
        self.get_stacked_sprite_cache(obj_names)

        for obj_name in obj_names:
            attrs = STACKED_SPRITE_ASSETS[obj_name]
            first_layout_img = self.byte_image_extraction(storage[obj_name]['0']['0'])
            for angle in range(NUM_ANGLES):

                surf = pg.Surface(first_layout_img.get_size())
                surf = pg.transform.rotate(surf, angle * VIEWING_ANGLE)
                sprite_surf = pg.Surface([surf.get_width(),
                                          surf.get_height() + attrs['num_layers'] * attrs['scale']])

                sprite_surf.fill('khaki')
                sprite_surf.set_colorkey('khaki')

                for idx in range(attrs['num_layers']):
                    layer_img = self.byte_image_extraction(storage[obj_name][str(angle)][str(idx)])
                    layer = pg.transform.rotate(layer_img, angle * VIEWING_ANGLE)
                    sprite_surf.blit(layer, (0, idx * attrs['scale']))

                image = pg.transform.flip(sprite_surf, True, True)

                self.stacked_sprite_cache[obj_name]['rotated_sprites'][angle] = image


if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode(RES)
    # store = ByteStorage()
    # store.save_database()
    #cache = Cache()
    app = PreloadedSprites()


