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
        self.agent_info = AgentInfo()    # table

        # TODO : portfolio indicators
        # self.portfolio_rets = PortfolioRets()

        self.load_real_stream_data()
        # self.exchange = exchange
        self.t = 0

    def load_real_stream_data(
        self,
    ) -> None:
        """Initialize trading data set.
        """

        self.real_stream_data = []
        data_size = 10000
        # TODO : csv file 
        for t in range(data_size):
            obs = dict(
                order_book=np.sort(np.random.random_sample(21)*100).tolist(),
                statistics=dict(ma10=100.0, std10=5.0),
            )   
            self.real_stream_data.append(obs)

    def observe(
        self,
    ):
        # TODO : optimize for low latency

        # SELECT * FROM agent_info WHERE agent_id='seoul_ai'
        cash = self.agent_info.cash
        asset_qtys = self.agent_info.asset_qtys
        asset_qty = asset_qtys.get("KRW-BTC")
        agent_info={"cash":cash, "asset_qtys":asset_qtys}

        obs = self.real_stream_data[self.t]

        # SELECT * FROM order_book WHERE ticker='KRW-BTC'
        # OR SELECT * FROM order_book_log WHERE ticker='KRW-BTC' LIMIT 1
        order_book = obs.get("order_book")
        cur_price = order_book[0+1]    # index + (order book size/2)
        portfolio_val = cash + (asset_qty * cur_price)
        # portfolio_val = cash + np.sum([asset_qty * cur_price[ticker] for ticker, asset_qty in asset_qtys.items()])

        # TODO : design portfolio rets schema.
        portfolio_rets={"val":portfolio_val, "mdd":0.0, "sharp":0.0}

        agent_data = dict(
            agent_info=agent_info,
            portfolio_rets=portfolio_rets,
        )
        obs.update(agent_data)

        self.t += 1

        return obs
