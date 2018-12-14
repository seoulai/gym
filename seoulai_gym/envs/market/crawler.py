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

        upbit_csv = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "test3.csv"))
        df = pd.read_csv(upbit_csv)
        data_size = len(df)

        # preprocess
        df[['ask_price', 'bid_price', 'price']] = \
            df[['ask_price', 'bid_price', 'price']].astype(dtype=int)

        # split
        order_book = df[['ask_price', 'ask_size', 'bid_price', 'bid_size']]
        order_book = order_book.to_dict(orient='records')
        trade = df[['price', 'volume']]
        trade = trade.to_dict(orient='records')

        real_stream_data = []
        for t in range(data_size):
            obs = dict(
                order_book=order_book[t],
                trade=trade[t],
                )
            real_stream_data.append(obs)

        return real_stream_data

    def scrap(
        self,
    ):
        cur_data = self.data[self.t]

        # UPDATE
        self.db.order_book = cur_data.get("order_book")
        self.db.trade = cur_data.get("trade")

        # TODO : INSERT TO LOG TABLE

        self.t += 1

