"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
from typing import List
from typing import Tuple
from pathlib import Path

import pygame

from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.base import Piece


class Graphics(Constants):
    def __init__(
        self,
        num_squares: int=8,
        window_size: int=600,
        board_image: str="board.png",
    ):
        self.num_squares = num_squares
        self.window_size = window_size
        self.square_size = self.window_size // self.num_squares
        self.piece_size = self.square_size // 2
        self.board_image = str(Path(__file__).parent / board_image)
        self.initialized_window = False

    def _init_window(
        self,
    ):
        """Initialize window separately from constructor. Window is initialized only when graphics
        is rendered for the first time.

        Returns:
            None
        """
        if not self.initialized_window:
            pygame.init()
            pygame.display.set_caption("Checkers")
            self.screen = pygame.display.set_mode([self.window_size] * 2)
            self.background = pygame.image.load(self.board_image)
            self._setup_colors()

    def _setup_colors(
        self,
    ) -> None:
        """Setup colors used for drawing pieces and squares.

        Returns: None
        """
        self.dark_piece_color = (0, 0, 0)
        self.light_piece_color = (255, 255, 255)
        self.king_piece_color = (64, 64, 64)
        self.original_piece_square_color = (160, 0, 255)
        self.possible_moves_square_color = (160, 190, 255)

    def update(
        self,
        board: List[List],
        orig_loc: Tuple[int, int],
        possible_moves: List[Tuple[int, int]],
    ) -> None:
        """Update visualization of board with respect to the current state.
        Pieces and possible moves for selected piece are displayed.

        Args:
            board: Information about positions of pieces.
            orig_loc: Original location of piece.
            possible_moves: Possible final destinations of selected piece.

        Returns:
            None
        """
        self._init_window()
        self.screen.blit(self.background, (0, 0))
        if orig_loc is not None and possible_moves is not None:
            if len(possible_moves) >= 1:
                self._highlight_possible_moves(*orig_loc, possible_moves)

        self._draw_pieces(board)
        pygame.display.update()

    def _highlight_possible_moves(
        self,
        orig_row: int,
        orig_col: int,
        possible_moves: List[Tuple[int, int]],
    ) -> None:
        """Highlight given squares.

        Args:
            orig_row: Row of original piece location.
            orig_col: Column of original piece location.
            squares: List of possible final destinations of piece.

        Returns:
            None
        """
        def draw_rect(row, col, color):
            pygame.draw.rect(
                self.screen,
                color,
                (col*self.square_size,
                 row*self.square_size,
                 self.square_size,
                 self.square_size))

        for row, col in possible_moves:
            draw_rect(row, col, self.possible_moves_square_color)

        draw_rect(orig_row, orig_col, self.original_piece_square_color)

    def _draw_pieces(
        self,
        board: List[List],
    ) -> None:
        """Draw current state (pieces) of board.

        Args:
            board: information about positions of pieces.
        """
        def get_pixel_coord(piece_pos: int):
            return int(piece_pos * self.square_size + self.piece_size)

        for row in range(self.num_squares):
            for col in range(self.num_squares):
                if board[row][col] is not None:
                    pygame.draw.circle(
                        self.screen,
                        self._get_piece_color(board[row][col]),
                        (get_pixel_coord(col), get_pixel_coord(row)),
                        self.piece_size)

                    if board[row][col].king:
                        pygame.draw.circle(
                            self.screen,
                            self.king_piece_color,
                            (get_pixel_coord(col), get_pixel_coord(row)),
                            self.piece_size // 2)

    def _get_piece_color(
        self,
        piece: Piece,
    ) -> Tuple[int, int, int]:
        """Get color of piece based on its type.

        Args:
            piece: Dark or light piece.

        Returns:
            color: Color of piece.

        Raises:
            ValueError: If given type is invalid.
        """
        if piece.ptype == self.DARK:
            color = self.dark_piece_color
        elif piece.ptype == self.LIGHT:
            color = self.light_piece_color
        else:
            raise ValueError("Unknown piece type.")

        return color
