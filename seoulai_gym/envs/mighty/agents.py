"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""
import random
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Tuple
from typing import Dict

from seoulai_gym.envs.mighty.base import Constants
from seoulai_gym.envs.mighty.rules import Rules


class Agent(ABC, Rules):
    @abstractmethod
    def __init__(
        self,
        name: str,
        uid: int,
        #ptype: int,
    ):
        #self._ptype = ptype
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


