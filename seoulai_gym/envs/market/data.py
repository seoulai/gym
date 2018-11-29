"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import pandas as pd
import numpy as np
import os

from seoulai_gym.envs.market.base import Constants
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
        # agent_info table 
        self.agent_info = dict(
            cash=100_000_000,
            asset_qtys={"KRW-BTC":0.0},
        )

        # portfolio table 
        self.portfolio_rets = dict(
             val=100_000_000,
             mdd=0.0,
             sharp=0.0,
        )

        self.load_real_stream_data()
        # self.exchange = exchange
        self.t = 0

    def load_real_stream_data(
        self,
    ) -> None:
        """Initialize trading data set.
        """

        self.real_stream_data = []
        data_size = 1000
        # TODO : csv file 
        for t in range(data_size):
            obs = dict(
                order_book=np.sort(np.random.random_integers(3_900_000, 5_000_000, 3)).tolist(),
                statistics=dict(ma10=np.random.random_sample()*100, std10=np.random.random_sample()*5),
            )   
            self.real_stream_data.append(obs)

    def observe(
        self,
    ):
        BASE = Constants.BASE
        # TODO : optimize for low latency

        # SELECT * FROM agent_info WHERE agent_id='seoul_ai'
        agent_info = self.agent_info
        cash = agent_info.get("cash")
        asset_qtys = agent_info.get("asset_qtys")
        asset_qty = asset_qtys.get("KRW-BTC")

        obs = self.real_stream_data[self.t]

        # SELECT * FROM order_book WHERE ticker='KRW-BTC'
        # OR SELECT * FROM order_book_log WHERE ticker='KRW-BTC' LIMIT 1
        order_book = obs.get("order_book")
        cur_price = order_book[0+1]    # index + (order book size/2)
        asset_qty0 = int(asset_qty*BASE)
        asset_val0 = int(asset_qty0*cur_price)
        cash0 = int(cash*BASE)
        portfolio_val = (cash0 + asset_val0)/BASE
        # portfolio_val = cash + np.sum([asset_qty * cur_price[ticker] for ticker, asset_qty in asset_qtys.items()])

        # TODO : design portfolio rets schema.
        self.portfolio_rets={"val":portfolio_val, "mdd":0.0, "sharp":0.0}
        portfolio_rets = self.portfolio_rets

        agent_data = dict(
            agent_info=agent_info,
            portfolio_rets=portfolio_rets,
        )
        obs.update(agent_data)

        self.t += 1

        return obs
