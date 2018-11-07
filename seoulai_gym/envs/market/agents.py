"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
from abc import ABC
from abc import abstractmethod
from seoulai_gym.envs.market.api import BaseAPI
from seoulai_gym.envs.market.base import Constants


class Agent(ABC, BaseAPI, Constants):
    def __init__(
        self,
        agent_id: str,
    ):
        self._agent_id = agent_id
        data = dict(agent_id=agent_id,)
        self.api_post("participate", data)

        self.actions = {}
        self.define_action()
        self.action_spaces = len(self.actions)
        self.action_keys = list(self.actions.keys())

        # self.define_state()
        # self.define_reward()

    def define_state(
        self,
        obs,
    ):
        state = obs
        return state

    @abstractmethod
    def define_action(
        self,
    ):
        pass

    # TODO: simplify code
    def action(
        self,
        index,
    ):
        try:
            if type(index) == str:
                key = index
            else:
                key = self.action_keys[index]
            parameters = self.actions[key]
            return self.order(*parameters)
        # FIXME:
        except IndexError:
            raise "index error!!!"

    def order(
        self,
        order_type: str,
        ticker: str,
        order_percent: int,
        d: int,
    ):
        self.validate(order_type, ticker, order_percent, d)

        if order_type == "buy":
            #  trad_price x trad_qty x (1+fee_rt) <= cash
            #  max_buy_qty = cash / {trad_price x (1+fee_rt)}

            trad_price = self.cur_price+self.tick*d
            max_buy_qty = self.cash / (trad_price * (1+self.fee_rt))
            trad_qty = max_buy_qty*(order_percent/100.0)
            return ticker, Constants.BUY, trad_qty, trad_price

        elif order_type == "sell":
            trad_price = self.cur_price+self.tick*d
            max_sell_qty = self.asset_qtys[ticker]
            trad_qty = max_sell_qty*(order_percent/100.0)
            return ticker, Constants.SELL, trad_qty, trad_price
        else:
            return ticker, Constants.HOLD, 0.0, 0.0

    def validate(
        self,
        order_type: str,
        ticker: str,
        order_percent: int,
        d: int,
    ):
        pass

    @abstractmethod
    def algo(
        self,
        state,
    ):
        pass

    def get_common(
        self,
        obs,
    ):
        self.fee_rt = obs.get("fee_rt")    # FIXME: unnecessary repeated assign
        self.cash = obs.get("cash")

        # self.asset_qtys = obs.get("asset_qty")
        self.asset_qtys = dict(
            BTC=100,
            ETH=20,)

        # DotDict(post_data.get("ticks"))
        self.cur_price = obs.get("cur_price")
        self.tick = 10.0    # a + nd

    # FIXME: participants shouldn't define act method
    def act(
        self,
        obs,
    ) -> None:
        if self.action_spaces == 0:
            raise AttributeError(f"actions does not exists")

        self.get_common(obs)
        state = self.define_state(obs)
        # TODO : simplify code.
        ticker, decision, trad_qty, trad_price = self.algo(state)
        action = (self._agent_id, ticker, decision, trad_qty, trad_price)
        return action

    @property
    def name(self, _agent_id):
        return _agent_id

    def __str__(self):
        return self._agent_id
