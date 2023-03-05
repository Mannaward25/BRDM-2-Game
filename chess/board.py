from settings import *
from square import Square
from pieces import *


class Board:

    def __init__(self):
        self.squares = list()
        self._create()
        self._add_pieces(PIECE_WHITE)
        self._add_pieces(PIECE_BLACK)

    def _create(self):
        self.squares = [[0] * ROWS for col in range(COLS)]

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == PIECE_WHITE else (1, 0)

        # pawns
        self._set_pieces(Pawn, row_pawn, color)

        # rooks
        self._set_pieces(Rook, row_other, color)

        # knights
        self._set_pieces(Knight, row_other, color)

        # bishops
        self._set_pieces(Bishop, row_other, color)

        # queen
        queen_col = Queen.PLACE_IN_COL
        self.squares[row_other][queen_col] = Square(row_other, queen_col, Queen(color))

        # king
        king_col = King.PLACE_IN_COL
        self.squares[row_other][king_col] = Square(row_other, king_col, King(color))

    def _set_pieces(self, piece: callable, row, color):
        for col in piece.PLACE_IN_COL:
            self.squares[row][col] = Square(row, col, piece(color))


if __name__ == '__main__':
    o = Board()
