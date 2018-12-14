"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""

import logging
from math import floor
from abc import ABC
from abc import abstractmethod
from seoulai_gym.envs.market.api import BaseAPI
from seoulai_gym.envs.market.base import Constants, fee_rt


class Agent(ABC, BaseAPI, Constants):
    def __init__(
        self,
        agent_id: str,
        actions: dict,
    ):
        self._agent_id = agent_id
        self._set_actions(actions)
        self.fee_rt = fee_rt

        # TODO : to tracking algo
        # data = dict(agent_id = agent_id)
        # self.api_post = ("submit", data)

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

    def _set_actions(
        self,
        actions:dict,
    ):
        # validate type of actions.
        if type(actions) != dict:
            raise AttributeError(f"you must return dictionary!!!")

        # validate empty actions.
        action_spaces = len(actions)
        if action_spaces == 0:
            raise AttributeError(f"you didn't define actions!!!")
        self.action_spaces = action_spaces

        # validate holding action.
        hold_action_list = [key for key, value in actions.items() if value in [0, (0, '%')]]
        if len(hold_action_list) == 0:
            raise AttributeError(f"you didn't define hold action!!! you must define : your_hold_action_name = 0 or (0, '%')")
        if len(hold_action_list) > 1:
            raise AttributeError(f"you defined duplicated hold action!!! Check your actions dictionary")

        self.actions = actions

        self.action_names = list(self.actions.keys())
        hold_action_key = hold_action_list[0]
        self.hold_action_index = self.action_names.index(hold_action_key)


    # TODO: simplify code
    def action(
        self,
        index,
    ):
        try:
            if type(index) == str:
                key = index
                index = self.action_names.index(index)
            else:
                key = self.action_names[index]

            parameters = self.actions[key]
            return self.orders(index, parameters)
        # FIXME:
        except IndexError:
            raise "index error!!!"

    def orders(
        self,
        index: int,
        parameters: tuple,
        ticker: str = "KRW-BTC",
    ):

        if type(parameters) in [float, int]:
            qty = parameters
            return self.order(index, qty)

        elif type(parameters) == tuple and len(parameters) == 1 and type(parameters[0]) == float:
            qty = parameters[0]
            return self.order(index, qty)

        elif type(parameters) == tuple and len(parameters) == 2 and parameters[1] == '%':
            percent = parameters[0]
            return self.order_percent(index, percent)

        else:
            raise AttributeError(f"parameters are incorrect!!")


    def order(
        self,
        index: int,
        qty: float = 0.0,
        ticker: str = "KRW-BTC",
    ):
        self.validate_order(qty, ticker)

        # initialize
        decision = Constants.HOLD
        trad_qty = 0.0
        trad_price = 0
        can_trade = False

        # HOLD 
        if index == self.hold_action_index:
            return index, ticker, decision, trad_qty, trad_price

        # BUY
        if self.cash >= 1000 and qty > 0:    # minimal order price = 1,000 KRW
            #  trad_price x trad_qty x (1+fee_rt) <= cash
            #  max_buy_qty = cash / {trad_price x (1+fee_rt)}

            decision = Constants.BUY
            trad_price = self.order_book.get("ask_price")
            trad_price = int(trad_price)
            max_buy_qty = self.cash / (trad_price * (1 + self.fee_rt))

            if qty <= max_buy_qty:
                trad_qty = qty
                trad_qty = floor(trad_qty*10000)/10000.0
                can_trade = True

        # SELL 
        elif self.asset_qtys[ticker] > 0 and qty < 0:
            decision = Constants.SELL
            trad_price = self.order_book.get("bid_price")
            trad_price = int(trad_price)

            max_sell_qty = self.asset_qtys[ticker]
            if abs(qty) <= max_sell_qty:
                trad_qty = abs(qty)
                trad_qty = floor(trad_qty*10000)/10000.0
                can_trade = True

        # can trade. but, calculated trading quantity = 0
        if (can_trade and int(trad_qty*10000) == 0):
            can_trade = False

        # can't trade
        if not can_trade:
            index = self.hold_action_index
            decision = Constants.HOLD
            trad_qty = 0.0
            trad_price = 0

        return index, ticker, decision, trad_qty, trad_price

    def validate_order(
        self,
        qty: float,
        ticker: str,
    ):
        qty = abs(qty)
        if int(qty*100000) > int(qty*10000)*10:
            raise Exception("invalid order definition!!! : we support only the 4th decimal place")

        if ticker not in ["KRW-BTC"]: 
            raise Exception("invalid ticker!!! : ticker = KRW-BTC")

    def order_percent(
        self,
        index: int,
        percent: int = 0,
        ticker: str = "KRW-BTC",
    ):
        self.validate_percent(percent, ticker)

        # initialize
        decision = Constants.HOLD
        trad_qty = 0.0
        trad_price = 0
        can_trade = False

        # HOLD 
        if index == self.hold_action_index:
            return index, ticker, decision, trad_qty, trad_price

        # BUY
        if self.cash >= 1000 and percent > 0:    # minimal order price = 1,000 KRW
            #  trad_price x trad_qty x (1+fee_rt) <= cash
            #  max_buy_qty = cash / {trad_price x (1+fee_rt)}

            decision = Constants.BUY
            trad_price = self.order_book.get("ask_price")
            trad_price = int(trad_price)
            max_buy_qty = self.cash / (trad_price * (1 + self.fee_rt))
            trad_qty = max_buy_qty*(percent/100.0)
            trad_qty = floor(trad_qty*10000)/10000.0
            can_trade = True

        # SELL 
        elif self.asset_qtys[ticker] > 0 and percent < 0:
            decision = Constants.SELL
            trad_price = self.order_book.get("bid_price")
            trad_price = int(trad_price)
            max_sell_qty = self.asset_qtys[ticker]
            trad_qty = max_sell_qty*(-percent/100.0)
            trad_qty = floor(trad_qty*10000)/10000.0
            can_trade = True

        # can trade. but, calculated trading quantity = 0
        if (can_trade and int(trad_qty*10000) == 0):
            can_trade = False

        # can't trade
        if not can_trade:
            index = self.hold_action_index
            decision = Constants.HOLD
            trad_qty = 0.0
            trad_price = 0

        return index, ticker, decision, trad_qty, trad_price

    def validate_percent(
        self,
        percent: float,
        ticker: str,
    ):
        percent = abs(percent)
        if int(percent*100) < 0 or int(percent*100) > 100*100:
            raise Exception("invalid order percent!!! : -100 <= percent <= 100")

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
        self.order_book = obs.get("order_book")
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
        index, ticker, decision, trad_qty, trad_price = self.algo(state)
        action = dict(
            index=index,
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
