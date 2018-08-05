"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
from abc import ABC
from abc import abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    def __init__(
        self,
        name: str,
    ):
        self._name = name

    @abstractmethod
    def act(
        self,
        obs,
        reward: int,
        done: bool,
    ) -> None:
        pass

    def __str__(self):
        return self._name
