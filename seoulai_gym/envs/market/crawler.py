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
from seoulai_gym.envs.market.database import DataBase 

class DataCrawler():
    def __init__(
        self,
        db : DataBase
    ):

        self.db = db
        self.data = self.load_data()
        self.t = 0

    def load_data(
        self,
    ) -> None:
        """Load local data set.
        """

        real_stream_data = []
        data_size = 1000

        # TODO : csv file 
        for t in range(data_size):
            obs = dict(

                order_book=dict(
                    ask_price=np.random.random_integers(3_900_000, 5_000_000),
                    ask_size=999999999999.0,
                    bid_price=np.random.random_integers(3_900_000, 5_000_000),
                    bid_size=999999999999.0),

                trade=dict(
                    cur_price=np.random.random_integers(3_900_000, 5_000_000),
                    cur_volume=999999999999.0,
                ),

                statistics=dict(
                    macd_first=np.random.random_integers(10_000, 11_000),
                    macd_second=np.random.random_integers(10_000, 11_000),
                    macd_third=np.random.random_integers(10_000, 11_000),
                    stoch_first=np.random.random_integers(10_000, 11_000),
                    stoch_second=np.random.random_integers(10_000, 11_000),
                    ma=np.random.random_integers(3_900_000, 5_000_000),
                    sma=np.random.random_integers(3_900_000, 5_000_000),
                    rsi=np.random.random_integers(10_000, 11_000),
                    std=np.random.random_integers(10_000, 11_000),
                ),
            )   
            real_stream_data.append(obs)

        return real_stream_data

    def scrap(
        self,
    ):
        cur_data = self.data[self.t]

        # UPDATE
        self.db.order_book = cur_data.get("order_book")
        self.db.statistics = cur_data.get("statistics")
        self.db.trade = cur_data.get("trade")

        # TODO : INSERT TO LOG TABLE

        self.t += 1

