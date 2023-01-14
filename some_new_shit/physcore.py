import pygame
import pygame_lib as pl
import math
import time
from gamecore import *


class GeometricObject:
    ELLIPSE = 'ellipse'
    RECT = 'rect'
    POLYGON = 'polygon'
    LINE = 'line'

    def __init__(self, surface, color: ColorType, objsize: SizeType, coord: CoordType,
                 material, width, shape_type):
        self.parent_surface = surface
        self.color = color
        self.coords = coord
        self.x_coord, self.y_coord = coord.coord()
        self.size = objsize
        self.material = material
        self.physical_object = PhysicalObject(shape_type, self, self.material)
        self.geometric_entity = None
        self.width = width
        self.collide_array = []

    def init(self):
        pass

    def redraw(self, coord):
        pass

    def draw(self):
        pass

    def get_volume(self) -> float:
        pass

    def get_physical_object(self):
        pass

    def get_geometric_entity(self):
        return self.geometric_entity

    def gen_collide_array(self):
        pass

    def is_point_of_object(self, point) -> bool:
        pass


class EllipseObject(GeometricObject):
    TYPE = GeometricObject.ELLIPSE
    PI = math.pi

    def __init__(self, surface, color: ColorType, objsize: SizeType, coord: CoordType, width: int = 0,
                 material='universal'):
        super().__init__(surface, color, objsize, coord, material, width, self.TYPE)

    def __repr__(self):
        return f'<GeometricObject> <{self.TYPE}>'

    def __str__(self):
        return f'<GeometricObject> <{self.TYPE}>'

    def init(self):  # physical encapsulation
        self.geometric_entity = pygame.draw.rect(self.parent_surface, self.color.rgb(),
                                                 self.coords + self.size)
        self.gen_collide_array()
        return self.geometric_entity

    def get_physical_object(self):
        return self.physical_object

    def redraw(self, coord):
        pygame.draw.ellipse(self.parent_surface, self.color.rgb(), coord + self.size)

    def get_volume(self):   # actually squared size cause of 2d
        """get size of figure"""
        x, y = self.size.size()
        if self.size.is_symmetric():
            r = x / 2  # circle S = pi * r * r
            square = self.PI * math.pow(r, 2)
        else:
            square = self.PI * (x / 2) * (y / 2)  # ellipse S = pi * R * r
        return square

    def get_geometric_entity(self):
        return self.geometric_entity

    def gen_collide_array(self):
        x, y = self.size.size()

        if self.size.is_symmetric():
            for d in range(0, 360, 1):
                rad = math.radians(d)
                cos_x = math.cos(rad)
                sin_y = math.sin(rad)
                x_res = self.x_coord + (cos_x * (x / 2))
                y_res = self.y_coord + (sin_y * (x / 2))
                self.collide_array.append(CoordType(int(x_res), int(y_res)))

    def is_point_of_object(self, point: CoordType):
        center = self.coords
        radius_x, radius_y = self.size.size()

        if self.size.is_symmetric():  # for circles
            distance = point - center
            x, y = distance.coord()
            hypotenuse = math.pow(x, 2) + math.pow(y, 2)
            if hypotenuse <= radius_x:
                return True
            else:
                return False


class RectObject(GeometricObject):
    TYPE = GeometricObject.RECT

    def __init__(self, surface, color: ColorType, objsize: SizeType, coord: CoordType, width: int = 0,
                 material='universal'):
        super().__init__(surface, color, objsize, coord, material, width, self.TYPE)

    def __repr__(self):
        return f'<GeometricObject> <{self.TYPE}>'

    def __str__(self):
        return f'<GeometricObject> <{self.TYPE}>'

    def init(self):  # physical encapsulation
        self.geometric_entity = pygame.draw.rect(self.parent_surface, self.color.rgb(),
                                                 self.coords + self.size)
        self.gen_collide_array()
        return self.geometric_entity

    def redraw(self, coord):
        pygame.draw.rect(self.parent_surface, self.color.rgb(), coord + self.size)

    def get_volume(self):
        x, y = self.size.size()
        return x * y

    def get_physical_object(self):
        return self.physical_object

    def get_geometric_entity(self):
        return self.geometric_entity

    def is_point_of_object(self, point: CoordType) -> bool:  # FIXME
        size_x, size_y = self.size.size()
        
        point_x, point_y = point.coord()
        if point_x in range(self.x_coord, self.x_coord + size_x) and \
           point_y in range(self.y_coord, self.y_coord + size_y):
            return True
        else:
            return False

    def gen_collide_array(self):
        size_x, size_y = self.size.size()
        for x in range(self.x_coord, self.x_coord + size_x):
            for y in range(self.y_coord, self.y_coord + size_y):
                if x in range(self.x_coord, self.x_coord + size_x) and \
                        y == self.y_coord or y == self.y_coord + size_y:
                    self.collide_array.append(CoordType(x, y))


class Material:
    """material class"""
    UNIVERSAL = 'universal'

    def __init__(self, mtype=None):
        if not mtype:
            self.material_type = self.UNIVERSAL
        else:
            self.material_type = mtype

        if self.material_type == self.UNIVERSAL:
            self.density = 1  # kg/m3


class PhysicalObject:
    obj_count = 0
    PHYS_OBJECTS_CASH = []

    def __init__(self, shape, geometric_entity: GeometricObject, material):
        #  init
        if self not in self.PHYS_OBJECTS_CASH:
            self.PHYS_OBJECTS_CASH.append((geometric_entity, self))

        #  geometric
        self.shape = shape
        self.geometricObj = geometric_entity
        self.x = geometric_entity.x_coord
        self.y = geometric_entity.y_coord

        #  physical
        self.material_type = Material(material)
        self.gravity = Gravity()
        self.volume = 0
        self.density = self.material_type.density
        self.mass = 0
        self.energy = 0
        self.speed = 0
        self.collided = False
        self.point_of_collision = None

        # init functions
        self._form_mass()

    def __repr__(self) -> str:
        return f'<PhysicalObject> <{self.shape}> | coordinates: x:{self.x}; y:{self.y}> | '

    def __str__(self) -> str:
        return f'<PhysicalObject> <{self.shape}> | coordinates: x:{self.x}; y:{self.y}> | '

    def _form_mass(self):
        self.volume = self.geometricObj.get_volume()
        self.mass = self.volume * self.density

    def dynamic(self):
        self.geometricObj.collide_array.clear()
        self.geometricObj.x_coord = self.x + int(self.geometricObj.size.width / 2) + 1

        print(self.shape)
        if self.shape == GeometricObject.ELLIPSE:
            self.geometricObj.y_coord = self.y + int(self.geometricObj.size.height / 2) + 1
        elif self.shape == GeometricObject.RECT:
            self.geometricObj.y_coord = self.y + int(self.geometricObj.size.height)

        self.geometricObj.gen_collide_array()

        self.speed = self.gravity.acceleration(self.speed, self.mass)

        if self.collided:
            if self.speed > 0:
                self.collided = False

            if self.y < self.point_of_collision.coord()[1]:
                self.speed = int(-self.speed * 0.88)
            else:
                self.y += int(self.speed * 0.7)  #  KINETIC ENERGY
        else:
            self.point_of_collision = self.collisions_detection()  # FIXME everything is working just proceed

            self.y += int(self.speed)

        self.geometricObj.redraw(CoordType(self.x, self.y))

    def static(self):
        self.geometricObj.redraw(CoordType(self.x, self.y))

    def collisions_detection(self, cash=[]) -> CoordType:

        self_collide_array = self.geometricObj.collide_array[:]
        for pair in self.PHYS_OBJECTS_CASH:
            if self == pair[1]:
                continue
            else:
                for point in self_collide_array:
                    if pair[0].is_point_of_object(point):
                        print(f"Collision of {self} with {pair[1]} at {point} ")
                        self.collided = True
                        self.speed = int(-self.speed * 0.8)

                        return point


class Gravity:
    G = {'earth': 9.8}

    def __init__(self, g=None):
        if not g:
            self.g = self.G['earth']
        else:
            self.g = g

    def acceleration(self, speed, mass):
        speed += int((self.g * (mass / 1000)) / 10)
        return speed


if __name__ == '__main__':
    pass
