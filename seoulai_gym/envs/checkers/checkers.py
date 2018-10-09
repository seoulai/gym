"""
Checkers
https://en.wikipedia.org/wiki/Draughts

Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
import copy
from typing import Dict
from typing import List
from typing import Tuple

import pygame
from pygame.locals import QUIT

from seoulai_gym.envs.checkers.base import Piece
from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.board import Board
from seoulai_gym.envs.checkers.graphics import Graphics
from seoulai_gym.envs.checkers.rules import Rules


class Checkers(Constants, Rules):
    def __init__(
        self,
    ) -> None:
        """Initialize checkers board and its visualization.

        Returns:
            None
        """
        self.possible_moves = None
        self.piece_location = None

        self.board = Board()
        self.graphics = Graphics()

    def update_rewards(
        self,
        rewards_map: Dict,
    ) -> None:
        """Update rewards. Adding new reward is not allowed.

        If `rewards_map` contains reward that wasn't defined in `Rewards`,
        AttributeError will be raised.

        Args:
            rewards_map: (Dict)

        Returns:
            None

        Raises:
            AttributeError: If attempts to add new reward.
        """
        self.board.update_rewards(rewards_map)

    def step(
        self,
        agent,
        from_row: int,
        from_col: int,
        to_row: int,
        to_col: int,
    ) -> Tuple[List[List[Piece]], int, bool, Dict]:
        """Make a step (= move) within board.

        Args:
            agent: Agent making a move.
            from_row: Row of board of original piece location.
            from_col: Col of board of original piece location.
            to_row: Row of board of desired piece location.
            to_col: Col of board of desired piece location.

        Returns:
            obs: Information about positions of pieces.
            rew: Reward for perfomed step.
            done: Information about end of game.
            info: Additional information about current step.
        """
        self.possible_moves = self.get_valid_moves(self.board.board_list, from_row, from_col)
        self.piece_location = (from_row, from_col)
        obs, rew, done, info = self.board.move(agent.ptype, from_row, from_col, to_row, to_col)
        return copy.deepcopy(obs), rew, done, info

    def reset(
        self,
    ) -> List[List[Piece]]:
        """Reset all variables and initialize new game.

        Returns:
            obs: Information about positions of pieces.
        """
        self.board = Board()
        obs = self.board.board_list
        return obs

    def render(
        self,
    ) -> None:
        """Display current state of board.

        Returns:
            None
        """
        self.graphics.update(
            self.board.board_list,
            self.piece_location,
            self.possible_moves,
        )

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

    def close(
        self,
    ) -> None:
        pygame.display.quit()
        pygame.quit()
        # pygame has to be again initialized, otherwise window does not close
        pygame.init()
