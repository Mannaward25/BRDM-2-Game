import pygame as pg
from settings import *
from board import *


class Core:

    def __init__(self, game):
        self.game = game
        self.board = Board()

    def get_rect(self, col, row) -> tuple:
        return col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE

    def draw_bg(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = LIGHT_COLOR
                else:
                    color = DARK_COLOR

                pg.draw.rect(self.game.screen, color, self.get_rect(col, row))

    def render_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    img = pg.image.load(piece.texture)
                    img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)

                    self.game.screen.blit(img, piece.texture_rect)
