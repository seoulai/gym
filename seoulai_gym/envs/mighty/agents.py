"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""
from abc import ABC
from abc import abstractmethod

from seoulai_gym.envs.mighty.rules import Rules


class Agent(ABC, Rules):
    @abstractmethod
    def __init__(
        self,
        name: str,
        uid: int,
    ):
        self._name = name
        self._uid = uid
    
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
