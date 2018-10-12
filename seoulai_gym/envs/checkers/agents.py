"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Tuple

from seoulai_gym.envs.checkers.base import Constants
from seoulai_gym.envs.checkers.rules import Rules
from seoulai_gym.envs.checkers.utils import generate_random_move


class Agent(ABC, Constants, Rules):
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
    ):
        pass

    @abstractmethod
    def consume(
        self,
        obs,
        reward: float,
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
    def name(self):
        if self.ptype == self.DARK:
            return f"DARK {self._name}"
        elif self.ptype == self.LIGHT:
            return f"LIGHT {self._name}"

    def __str__(self):
        return self._name


class RandomAgent(Agent):
    def __init__(
        self,
        ptype: int,
    ):
        """Initialize random agent.

        Args:
            name: name of agent.
            ptype: type of piece that agent is responsible for.
        """
        if ptype == Constants().DARK:
            name = "RandomAgentDark"
        elif ptype == Constants().LIGHT:
            name = "RandomAgentLight"
        else:
            raise ValueError

        super().__init__(name, ptype)

    def act(
        self,
        board: List[List],
    ) -> Tuple[int, int, int, int]:
        """
        Choose a piece and its possible moves randomly.
        Pieces and moves are chosen from all current valid possibilities.

        Args:
            board: information about positions of pieces.

        Returns:
            Current and new location of piece.
        """
        rand_from_row, rand_from_col, rand_to_row, rand_to_col = generate_random_move(
            board,
            self.ptype,
            len(board),
        )
        return rand_from_row, rand_from_col, rand_to_row, rand_to_col

    def consume(
        self,
        obs: List[List],
        reward: float,
        done: bool,
    ) -> None:
        """Agent processes information returned by environment based on agent's latest action.
        Random agent does not need `reward` or `done` variables, but this method is called anyway
        when used with other agents.

        Args:
            board: information about positions of pieces.
            reward: reward for perfomed step.
            done: information about end of game.
        """
        pass


class RandomAgentLight(RandomAgent):
    def __init__(
        self,
    ):
        super().__init__(Constants().LIGHT)


class RandomAgentDark(RandomAgent):
    def __init__(
        self,
    ):
        super().__init__(Constants().DARK)
