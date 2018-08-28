"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
import numpy as np
from typing import List

from seoulai_gym.envs.checkers.base import Constants


def board_list2numpy(
    board_list: List[List],
) -> np.array:
    """TODO
    """
    constants = Constants()

    board_map = {
        constants.EMPTY: 0,

        constants.DARK: 10,
        constants.DARK_KING: 11,

        constants.LIGHT: 20,
        constants.LIGHT_KING: 21,
    }

    board_size = len(board_list)
    board_numpy = constants.EMPTY * np.ones((board_size, board_size))

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

                board_numpy[row][col] = board_map[piece_type]

    return board_numpy
