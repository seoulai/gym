"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
from math import floor
from abc import ABC
from abc import abstractmethod
from seoulai_gym.envs.market.api import BaseAPI
from seoulai_gym.envs.market.base import Constants


class Agent(ABC, BaseAPI, Constants):
    def __init__(
        self,
        agent_id: str,
        agent_key: str = "",
    ):
        self._agent_id = agent_id
        self._common_data_columns=["fee_rt", "cash", "asset_qtys", "cur_price", "order_book"]
        # self._agent_key = agent_key
        # data = dict(agent_id=agent_id)

        # TODO : to tracking algo
        # data = dict(agent_id = agent_id)
        # self.api_post = ("submit", data)

        self.actions = {}
        self.actions = self.set_actions()
        if type(self.actions) != dict:
            raise AttributeError(f"you must return dictionary!!!")
        self.action_spaces = len(self.actions)
        if self.action_spaces == 0:
            raise AttributeError(f"you didn't define actions")
        self.action_names = list(self.actions.keys())
        print(f"================================================================================================================")
        print(f"SEOUL AI HACKATHON FOR TRADING")
        print(f"actions_spaces = {self.action_spaces}")
        print(f"your_action_names = {self.action_names}")
        print(f"you can use common_columns in your agent class. common_columns = {self._common_data_columns}")
        print(f"================================================================================================================\n")

        self.fee_rt = 0.05/100

    def preprocess(
        self,
        obs,
    ):
        state = obs
        return state

    def postprocess(
        self,
        obs,
    ):
        state = obs
        return state

    @abstractmethod
    def set_actions(
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
                key = self.action_names[index]
            order_percent = self.actions[key]
            return self.order(order_percent)
        # FIXME:
        except IndexError:
            raise "index error!!!"

    def order(
        self,
        order_percent: int = 0,
        ticker: str = "KRW-BTC",
    ):
        self.validate(order_percent, ticker)

        # initialize
        decision = Constants.HOLD
        trad_qty = 0.0
        trad_price = 0

        # BUY
        if self.cash >= 1000 and order_percent > 0:    # minimal order price = 1,000 KRW
            #  trad_price x trad_qty x (1+fee_rt) <= cash
            #  max_buy_qty = cash / {trad_price x (1+fee_rt)}

            decision = Constants.BUY
            trad_price = self.order_book.get("ask_price")
            trad_price = int(trad_price)
            max_buy_qty = self.cash / (trad_price * (1 + self.fee_rt))
            trad_qty = max_buy_qty*(order_percent/100.0)
            trad_qty = floor(trad_qty*10000)/10000

        # SELL 
        elif self.asset_qtys[ticker] > 0 and order_percent < 0:
            decision = Constants.SELL
            trad_price = self.order_book.get("bid_price")
            trad_price = int(trad_price)
            max_sell_qty = self.asset_qtys[ticker]
            trad_qty = max_sell_qty*(-order_percent/100.0)
            trad_qty = floor(trad_qty*10000)/10000

        # HOLD
        if int(trad_qty*10000) == 0:
            decision = Constants.HOLD

        return ticker, decision, trad_qty, trad_price

    def validate(
        self,
        order_percent: int,
        ticker: str,
    ):
        if order_percent < -100 or order_percent > 100:
            raise Exception("invalid order percent!!! : -100 <= order_percent <= 100")

        if ticker not in ["KRW-BTC"]: 
            raise Exception("invalid ticker!!! : ticker = KRW-BTC")

    @abstractmethod
    def algo(
        self,
        state,
    ):
        pass

    def _get_common(
        self,
        obs,
    ):
        # print(obs)
        self.order_book = obs.get("order_book")

        self.trade= obs.get("trade")
        self.cur_price = self.trade.get("cur_price")
        self.cur_volume = self.trade.get("cur_volume")

        self.statistics = obs.get("statistics")
        self.ma = self.statistics.get("ma")
        self.sma = self.statistics.get("sma")
        self.std = self.statistics.get("std")

        self.agent_info = obs.get("agent_info")
        self.cash = self.agent_info["cash"]
        self.asset_qtys = self.agent_info.get("asset_qtys")

        self.portfolio_rets = obs.get("portfolio_rets")
        self.portfolio_val = self.portfolio_rets.get("val")

    # FIXME: participants shouldn't define act method
    def act(
        self,
        obs,
    ) -> None:
        if self.action_spaces == 0:
            raise AttributeError(f"actions does not exists")

        self._get_common(obs)
        state = self.preprocess(obs)
        # TODO : simplify code.
        ticker, decision, trad_qty, trad_price = self.algo(state)
        action = dict(
            agent_id=self._agent_id,
            ticker=ticker,
            decision=decision,
            trad_qty=trad_qty,
            trad_price=trad_price)
        return action

    @property
    def name(self, _agent_id):
        return _agent_id

    def __str__(self):
        return self._agent_id
