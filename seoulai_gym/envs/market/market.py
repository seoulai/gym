"""
Stock Market
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import copy
from typing import Dict
from typing import List
from typing import Tuple

import pygame
from pygame.locals import QUIT
import numpy as np

from seoulai_gym.envs.market.api import BaseAPI
from seoulai_gym.envs.market.base import Constants
from seoulai_gym.envs.market.price import Price, Exchange 
from seoulai_gym.envs.market.graphics import Graphics


class Market(BaseAPI):
    def __init__(
        self,
        state: str=None,
    ) -> None:
        """Initialize market and its visualization.
        Args:
            state: Optional, path to saved game state. TODO
        Returns:
            None
        """
        #self.traders = 0    # for multi-players

        # graphics is for visualization
        # self.graphics = Graphics()
        # self.pause = False  # pause game

    def select(
        self,
        exchange
    ) -> None:

        data = dict(exchange=exchange,
                   )
        self.fee_rt = self.api_get("select", data)

    def reset(
        self
    ):
        """Reset all variables and initialize new game.
        Returns:
            obs: Information about trading parameters.
        """
        data = {}
        state = self.api_post("reset", data)
 
        return state

    def step(
        self,
        agent,
        decision: int,
        trad_qty: float,
        trad_price: float,
    ):
        """Make a step (= move) within market.
        Args:
            agent: Agent name(id) 
            decision : buy, sell or hold. Agent position.
            trad_price: Price that Agent want to trade.
            trad_qty: Quantity that Agent want to trade.
        Returns:
            obs: Information of price history and fee ratio.
            rew: Reward for perfomed step.
            done: Information about end of game.
            info: Additional information about current step.
        """
        data = dict(agent=agent,
                    decision=decision,
                    trad_qty=trad_qty,
                    trad_price=trad_price,
                    )
        r = self.api_post("step", data)

        next_state = r.get("agent")
        reward = r.get("reward")
        done = r.get("done")
        info = r.get("info")

        return next_state, reward, done, info 

    def render(
        self,
        agent,
        info,
        decision,
    ) -> None:
        """Display current state of board.
        Returns:
            None
        """
        pass

    def paused(self):
        pass

    def close(
        self,
    ) -> None:
        pass
