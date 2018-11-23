"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import pandas as pd
import numpy as np
import os
from seoulai_gym.envs.market.dbclient import AgentInfo 


class Exchange(object):
    pass


class Bithumb(Exchange):
    fee_rt = 0.15/100


class Upbit(Exchange):
    fee_rt = 0.05/100


class Data():
    def __init__(
        self,
        # exchange: Exchange
    ):
        """Data constructor.

        Args:
            exchange: Exchange.
        """
        # self.stock_total_volume = 2000
        self.agent_info = AgentInfo()
        self.init()
        # self.exchange = exchange
        self.t = 0

    def init(
        self,
    ) -> None:
        """Initialize trading data set.
        """

        self.observations = []
        data_size = 1000
        # TODO : order_book -> list[list] : tickers
        for t in range(data_size):
            obs = dict(
                order_book=np.sort(np.random.random_sample(21)*100).tolist(),
                statistics=dict(ma10=100.0, std10=5.0),
            )   
            self.observations.append(obs)
        # print(self.observations)

    def get_obs(
        self,
    ):
        obs = self.observations[self.t]

        cash = self.agent_info.cash
        asset_qtys = self.agent_info.asset_qtys
        asset_qty = asset_qtys.get("KRW-BTC")    # FIXME : it's wrong.
        agent_info={"cash":cash, "asset_qtys":asset_qtys}

        # TODO : low latency
        order_book = obs.get("order_book")
        cur_price = order_book[0+10]
        portfolio_val = cash + (asset_qty * cur_price)
        portfolio_rets={"val":portfolio_val, "mdd":0.0, "sharp":0.0},

        agent_data = dict(
            agent_info=agent_info,
            portfolio_rets=portfolio_rets,
        )
        obs.update(agent_data)

        self.t += 1

        return obs
