from settings import *


class Piece:
    NAME = 'none'
    VALUE = 0
    PLACE_IN_COL = 0

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color

        value_sign = 1 if color == PIECE_WHITE else -1
        self.value = value * value_sign
        self.texture = texture
        self.get_texture_path()
        self.texture_rect = texture_rect

        self.valid_moves = []
        self.moved = False

    def get_texture_path(self, size=80):
        self.texture = f'resources/images/imgs-{size}px/{self.color}_{self.name}.png'

    def add_moves(self, move):
        self.valid_moves.append(move)


class Pawn(Piece):
    NAME = 'pawn'
    VALUE = 1.0
    PLACE_IN_COL = range(8)

    def __init__(self, color):
        self.dir = 1 if color == PIECE_BLACK else -1
        super().__init__(self.NAME, color, self.VALUE)


class Knight(Piece):
    NAME = 'knight'
    VALUE = 3.0
    PLACE_IN_COL = (1, 6)

    def __init__(self, color):
        super().__init__(self.NAME, color, self.VALUE)


class Bishop(Piece):
    NAME = 'bishop'
    VALUE = 3.001
    PLACE_IN_COL = (2, 5)

    def __init__(self, color):
        super().__init__(self.NAME, color, self.VALUE)


class Rook(Piece):
    NAME = 'rook'
    VALUE = 5.0
    PLACE_IN_COL = (0, 7)

    def __init__(self, color):
        super().__init__(self.NAME, color, self.VALUE)


class Queen(Piece):
    NAME = 'queen'
    VALUE = 9.0
    PLACE_IN_COL = 3

    def __init__(self, color):
        super().__init__(self.NAME, color, self.VALUE)


class King(Piece):
    NAME = 'king'
    VALUE = 100000.0
    PLACE_IN_COL = 4

    def __init__(self, color):
        super().__init__(self.NAME, color, self.VALUE)
