"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
import random
from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Tuple

from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.checkers import Checkers
from seoulai_gym.envs.checkers.rules import generate_valid_moves
from seoulai_gym.envs.checkers.rules import get_valid_moves
from seoulai_gym.envs.checkers.rules import get_between_position
from seoulai_gym.envs.checkers.rules import get_opponent_type
from seoulai_gym.envs.checkers.rules import get_positions
from seoulai_gym.envs.checkers.rules import validate_move


class Agent(Constants, ABC):
    @abstractmethod
    def __init__(
        self,
        name: str,
        ptype: int,
    ):
        self._ptype = ptype
        self._name = name

    @abstractmethod
    def act(
        self,
        obs,
        reward: int,
        done: bool,
    ) -> None:
        pass

    @property
    def ptype(self):
        return self._ptype

    @ptype.setter
    def ptype(self, _ptype):
        if _ptype == self.DARK or _ptype == self.LIGHT:
            return _ptype
        else:
            raise ValueError("Invalid piece type.")

    @property
    def name(self, _name):
        if self.ptype == self.DARK:
            return  f"DARK {_name}"
        elif self.ptype == self.LIGHT:
            return f"LIGHT {_name}"

    def __str__(self):
        return self._name


class RandomAgent(Agent):
    def __init__(
        self,
        name: str,
        ptype: int,
    ):
        """Initialize random agent.

        Args:
            name: name of agent.
            ptype: type of piece that agent is responsible for.
        """
        super().__init__(name, ptype)

    def act(
        self,
        board: List[List],
        reward: int,
        done: bool,
    ) -> Tuple[int, int, int, int]:
        """
        Choose a piece and its possible moves randomly.
        Pieces and moves are chosen from all current valid possibilities.

        Args:
            board: information about positions of pieces.
            reward: reward for perfomed step.
            done: information about end of game.

        Returns:
            Current and new location of piece.
        """
        board_size = len(board)
        valid_moves = generate_valid_moves(board, self.ptype, board_size)
        rand_from_row, rand_from_col = random.choice(list(valid_moves.keys()))
        rand_to_row, rand_to_col = random.choice(valid_moves[(rand_from_row, rand_from_col)])
        return rand_from_row, rand_from_col, rand_to_row, rand_to_col


class RandomAgentLight(RandomAgent):
    def __init__(
        self,
        name: str,
    ):
        super().__init__(name, Constants().LIGHT)


class RandomAgentDark(RandomAgent):
    def __init__(
        self,
        name: str,
    ):
        super().__init__(name, Constants().DARK)
