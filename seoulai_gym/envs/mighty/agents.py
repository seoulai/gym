"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""
from abc import abstractmethod

from seoulai_gym.envs.base_agent import BaseAgent


class Agent(BaseAgent):
    @abstractmethod
    def __init__(
        self,
        name: str,
        uid: int,
    ):
        super().__init__(name)
        self._uid = uid
