"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import numpy as np
import random
from abc import ABC
from abc import abstractmethod
from typing import Tuple

from seoulai_gym.envs.market.base import Constants


class Agent(ABC, Constants):
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

    @property
    def name(self, _name):
        return _name

    def __str__(self):
        return self._name


class RandomAgent(Agent):
    def __init__(
            self,
            name: str,
            init_cash: float,
    ):
        """Initialize random agent.

        Args:
            name: name of agent.
            ptype: type of piece that agent is responsible for.
        """
        super().__init__(name)
        self.init_cash = init_cash
        self.cash = init_cash
        self.asset_qty = 0.0
        self.asset_val = 0.0
        self.wallet_history = []

    def act(
        self,
        obs,  # price history
        reward: int,
        done: bool,
    ) -> Tuple[int, int, int]:
        """
        Args:
            prices: price data set of stock.
            reward: reward for perfomed step.
            done: information about end of game.

        Returns:
            Current and new location of piece.
        """

        # TODO : RL Algo
        decision = random.choice(
            list([Constants.BUY, Constants.SELL, Constants.HOLD]))

        price_list = obs[0]
        fee_rt = obs[1]

        trad_price = price_list[-1]    # select current price
        trad_qty = 0
        max_qty = 0

        # validation
        if decision == Constants.BUY:
            fee = trad_price*fee_rt    # calculate fee(commission)
            # max buy quantity = cash / (trading price + fee)
            max_qty = self.cash/(trad_price+fee)
        elif decision == Constants.SELL:
            max_qty = self.asset_qty

        # if max_qty >0 (you can trade), choose trading_qty randomly (0.0~max_qty)
        if max_qty > 0:
            trad_qty = np.random.random_sample() * max_qty
        else:
            # if max_qty = 0(you can't trade), you can't buy or sell.
            decision = Constants.HOLD

        # FIXME: wallet history should be updated after order is closed
        self.wallet_history.append(
            self.cash + self.asset_val)

        return decision, trad_price, trad_qty


class RandomAgentBuffett(RandomAgent):
    def __init__(
        self,
        name: str,
        init_cash: float,
    ):
        super().__init__(name, init_cash)


class RandomAgentSon(RandomAgent):
    def __init__(
        self,
        name: str,
    ):
        super().__init__(name)

class MRV1Agent(RandomAgent):
    def __init__(
        self,
        name: str,
        init_cash: float,
    ):
        super().__init__(name, init_cash)
    def act(
        self,
        obs,
        reward: int,
        done: bool,
    ) -> Tuple[int, int, int]:
        """
        Args:
            obs: data set of obsevation
            reward: reward for perfomed step.
            done: information about end of game.

        Returns:
            decision(direction), trading price, trading quantity
        """

        price_list = obs[0]
        fee_rt = obs[1]
        tick = obs[2]

        trad_price = price_list[-1]    # select current price
        trad_qty = 0
        #max_qty = 0

        # FIXME: wallet history should be updated after order is closed
        self.wallet_history.append(
            self.cash + self.asset_val)

        n = 10
        thresh_hold = 1.0

        # mean reverting algorithm
        if tick <= n:
            return Constants.HOLD, 0, 0
        
        cur_price = price_list[-1]
        price_n = price_list[:-n]
        avg_n = np.mean(price_n)
        std_n = np.std(price_n)

        if cur_price > avg_n + std_n*thresh_hold:
            decision = Constants.SELL
        elif cur_price < avg_n - std_n*thresh_hold:
            decision = Constants.BUY
        else:
            decision = Constants.HOLD

        # validation
        if decision == Constants.BUY:
            fee = trad_price*fee_rt    # calculate fee(commission)
            # max buy quantity = cash / (trading price + fee)
            trad_qty = self.cash/(trad_price+fee)
        elif decision == Constants.SELL:
            trad_qty = self.asset_qty

        return decision, trad_price, trad_qty
