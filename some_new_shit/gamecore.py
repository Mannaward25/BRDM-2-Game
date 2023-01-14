

class SizeType:
    """base size type"""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f'<SizeType> (w:{self.width}, h:{self.height})'

    def __str__(self) -> str:
        return f'<SizeType> (w:{self.width}, h:{self.height})'

    def __add__(self, other):
        if isinstance(other, CoordType):
            return RectType(*other.coord(), *self.size()).rect()

    def size(self) -> tuple:
        """return width and height"""
        return self.width, self.height

    def is_symmetric(self) -> bool:
        """is sizes equal?"""
        return self.width == self.height


class RectType:
    """base rect type"""
    def __init__(self, x_coord, y_coord, width, height):
        self.x = x_coord
        self.y = y_coord
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f'<RectType> (x:{self.x}, y:{self.y}, w:{self.width}, h:{self.height})'

    def __str__(self) -> str:
        return f'<RectType> (x:{self.x}, y:{self.y}, w:{self.width}, h:{self.height})'

    def rect(self) -> tuple:
        return self.x, self.y, self.width, self.height


class CoordType:
    """base coord type"""

    def __init__(self, coord_x, coord_y):
        self.x, self.y = coord_x, coord_y

    def __repr__(self) -> str:
        return f'<CoordType> ({self.x}, {self.y})'

    def __str__(self) -> str:
        return f'<CoordType> ({self.x}, {self.y})'

    def __add__(self, other):
        if isinstance(other, CoordType):
            self_x, self_y = self.coord()
            other_x, other_y = other.coord()
            #res = (self_x + other_x, self_y + other_y)
            return CoordType(self_x + other_x, self_y + other_y)
        elif isinstance(other, SizeType):
            self_coord = self.coord()
            other_size = other.size()
            return RectType(*self_coord, *other_size).rect()

    def __sub__(self, other):
        if isinstance(other, CoordType):
            self_x, self_y = self.coord()
            other_x, other_y = other.coord()
            return CoordType(self_x - other_x, self_y - other_y)

    def coord(self) -> tuple:
        return self.x, self.y


class ColorType:
    """base color type"""

    def __init__(self, rgb):
        if isinstance(rgb, ColorType):
            self.r, self.g, self.b = rgb.rgb()
        elif isinstance(rgb, tuple):
            self.r, self.g, self.b = rgb

    def __repr__(self) -> str:
        return f'<ColorType> (r:{self.r}, g:{self.g}, b:{self.b})'

    def __str__(self) -> str:
        return f'<ColorType> (r:{self.r}, g:{self.g}, b:{self.b})'

    def __add__(self, other):
        if isinstance(other, ColorType):
            t1 = self.rgb()
            t2 = other.rgb()
            res = tuple(map(lambda v1, v2: int((v1 + v2) / 2), t1, t2))
            return ColorType(res)

    def rgb(self) -> tuple:
        return self.r, self.g, self.b


if __name__ == '__main__':
    pass
