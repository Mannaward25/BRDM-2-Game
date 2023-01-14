import pygame
import math
from gamecore import *


class GeometricObject:
    ELLIPSE = 'ellipse'
    RECT = 'rect'
    POLYGON = 'polygon'
    LINE = 'line'

    def __init__(self, surface, color: ColorType, objsize: SizeType, coord: CoordType, material):
        self.parent_surface = surface
        self.color = color
        self.coords = coord
        self.x_coord, self.y_coord = coord.coord()
        self.size = objsize
        self.material = material
        self.physical_object = None

    def draw(self):
        pass

    def get_volume(self) -> float:
        pass


class EllipseObject(GeometricObject):
    TYPE = GeometricObject.ELLIPSE
    PI = math.pi

    def __init__(self, surface, color: ColorType, objsize: SizeType, coord: CoordType, width: int = 0,
                 material='universal'):
        super().__init__(surface, color, objsize, coord, material)
        self.width = width

    def init(self):  # physical encapsulation
        self.physical_object = PhysicalObject(self.TYPE, self, self.material)
        rect_obj = self.coords + self.size
        rgb = self.color.rgb()
        return pygame.draw.ellipse(self.parent_surface, rgb, rect_obj)

    def get_physical_object(self):
        if self.physical_object:
            return self.physical_object
        else:
            return None

    def _redraw(self):
        pass

    def redraw(self, coord):
        rect_obj = coord + self.size
        rgb = self.color.rgb()
        pygame.draw.ellipse(self.parent_surface, rgb, rect_obj)

    def get_volume(self):   # actually squared size cause of 2d
        """get size of figure"""
        x, y = self.size.size()
        if self.size.is_symmetric():
            r = x / 2  # circle S = pi * r * r
            square = self.PI * math.pow(r, 2)
        else:
            square = self.PI * (x / 2) * (y / 2)  # ellipse S = pi * R * r
        return square


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
    G = 9.8

    def __init__(self, shape, geometric_entity: GeometricObject, material):
        #  geometric
        self.shape = shape
        self.geometricObj = geometric_entity

        #  physical
        self.material_type = Material(material)
        self.volume = 0
        self.density = self.material_type.density
        self.mass = 0
        self.energy = 0
        self.speed = 0

        # init functions
        self._form_mass()

    def _form_mass(self):
        self.volume = self.geometricObj.get_volume()
        self.mass = self.volume * self.density


class Force:
    pass


if __name__ == '__main__':
    pass
