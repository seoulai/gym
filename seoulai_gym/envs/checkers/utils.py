"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
import random
from typing import List

import numpy as np

from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.rules import Rules


class BoardEncoding(object):
    def __init__(self):
        self._constants = Constants()
        self._encoding = {}

        self.empty = 0
        self.dark = 10
        self.dark_king = 11
        self.light = 20
        self.light_king = 21

    def __getitem__(self, name):
        return self._encoding[name]

    @property
    def empty(self):
        return self._encoding[self._constants.EMPTY]

    @empty.setter
    def empty(self, value):
        self._encoding[self._constants.EMPTY] = value

    @property
    def dark(self):
        return self._encoding[self._constants.DARK]

    @dark.setter
    def dark(self, value):
        self._encoding[self._constants.DARK] = value

    @property
    def dark_king(self):
        return self._encoding[self._constants.DARK_KING]

    @dark_king.setter
    def dark_king(self, value):
        self._encoding[self._constants.DARK_KING] = value

    @property
    def light(self):
        return self._encoding[self._constants.LIGHT]

    @light.setter
    def light(self, value):
        self._encoding[self._constants.LIGHT] = value

    @property
    def light_king(self):
        return self._encoding[self._constants.LIGHT_KING]

    @light_king.setter
    def light_king(self, value):
        self._encoding[self._constants.LIGHT_KING] = value


def board_list2numpy(
    board_list: List[List],
    encoding: BoardEncoding=BoardEncoding(),
) -> np.array:
    """Convert the state of game (`board_list`) into 2D NumPy Array using `encoding`.

    Args:
        board_list: (List[List[Piece]]) State of the game.
        encoding: (BoardEncoding) Optional argument. If not given default encoding will be utilized.

    Returns:
        board_numpy: (np.array)
    """
    board_size = len(board_list)
    constants = Constants()
    board_numpy = encoding[constants.EMPTY] * np.ones((board_size, board_size))

    for row in range(board_size):
        for col in range(board_size):
            if board_list[row][col] is not None:
                ptype = board_list[row][col].ptype
                king = board_list[row][col].king

                if ptype == constants.LIGHT:
                    if king:
                        piece_type = constants.LIGHT_KING
                    else:
                        piece_type = constants.LIGHT
                else:  # DARK
                    if king:
                        piece_type = constants.DARK_KING
                    else:
                        piece_type = constants.DARK

                board_numpy[row][col] = encoding[piece_type]

    return board_numpy


def generate_random_move(
    board: List[List],
    ptype: int,
    board_size: int,
):
    """Generate random move from all `ptype` valid moves but does not execute it.

    Args:
        board: (List[List[Piece]]) State of the game.
        ptype: (int) type of piece for which random move will be generated
        board_size: (int) size of board
    """
    valid_moves = Rules.generate_valid_moves(board, ptype, board_size)
    rand_from_row, rand_from_col = random.choice(list(valid_moves.keys()))
    rand_to_row, rand_to_col = random.choice(valid_moves[(rand_from_row, rand_from_col)])
    return rand_from_row, rand_from_col, rand_to_row, rand_to_col
