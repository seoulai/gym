"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
import numpy as np
from typing import Tuple
from typing import Dict
from typing import List

from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.base import DarkPiece
from seoulai_gym.envs.checkers.base import LightPiece
from seoulai_gym.envs.checkers.rules import get_between_position
from seoulai_gym.envs.checkers.rules import get_opponent_type
from seoulai_gym.envs.checkers.rules import get_positions
from seoulai_gym.envs.checkers.rules import validate_move
from seoulai_gym.envs.checkers.rules import generate_valid_moves


class Board(Constants):
    def __init__(
        self,
        size: int=8,
    ):
        """Board constructor.

        Args:
            size: Board size.
        """
        self.size = size
        self.init()

    def init(
        self,
    ) -> None:
        """Initialize board and setup pieces on board.

        Note: Dark pieces should be ALWAYS on the top of the board.
        """
        self.board_list = [
            [DarkPiece(), None] * (self.size//2),
            [None, DarkPiece()] * (self.size//2),
            [DarkPiece(), None] * (self.size//2),
            [None] * self.size,
            [None] * self.size,
            [None, LightPiece()] * (self.size//2),
            [LightPiece(), None] * (self.size//2),
            [None, LightPiece()] * (self.size//2),
        ]

    def move(
        self,
        ptype: int,
        from_row: int,
        from_col: int,
        to_row: int,
        to_col: int,
    ) -> Tuple[List[List], int, bool, Dict]:
        """Move piece across board and check validity of movement.

        Args:
            ptype: Type of piece making a move.
            from_row: Row of board of original piece location.
            from_col: Column of board of original piece location.
            to_row: Row of board of desired piece location.
            to_col: Column of board of desired piece location.

        Returns:
            obs: information about positions of pieces.
            rew: reward for perfomed step.
            done: information about end of game.
            info: additional information about current step.

        Raises:
            ValueError: If given movement is not valid.
        """
        rew = 0  # TODO compute reward
        info = {}

        if not validate_move(self.board_list, from_row, from_col, to_row, to_col):
            raise ValueError(f"Attempt to move to invalid position.")
        else:
            info.update({"moved": ((from_row, from_col), (to_row, to_col))})

        # don't move with opponent's piece
        if ptype != self.board_list[from_row][from_col].ptype:
            raise ValueError("Attempt to move with opponent's piece.")

        # move
        self.board_list[to_row][to_col] = self.board_list[from_row][from_col]
        self.board_list[from_row][from_col] = None

        # remove opponent's piece
        between_row, between_col = get_between_position(from_row, from_col, to_row, to_col)
        if between_row is not None and between_col is not None:
            p_between = self.board_list[between_row][between_col]
            if p_between is not None:
                self.board_list[between_row][between_col] = None
                info.update({"removed": ((between_row, between_col), p_between)})

        # become king
        p = self.board_list[to_row][to_col]
        if (to_row == 0 and p.direction == self.UP) or (to_row == self.size-1 and p.direction == self.DOWN):
            p.make_king()
            info.update({"king": (to_row, to_col)})

        # end of game?
        if len(get_positions(self.board_list, get_opponent_type(p.ptype), self.size)) == 0:
            # opponent lost all his pieces
            done = True
        elif len(generate_valid_moves(self.board_list, get_opponent_type(p.ptype), self.size)) == 0:
            # opponent cannot make any move
            done = True
        else:
            done = False

        obs = self.board_list
        return obs, rew, done, info
