"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import pandas as pd
from seoulai_gym.envs.market.base import Constants
import os


class Price(Constants):
    def __init__(
        self,
        price_list_size: int=1000,  # trading game size
    ):
        """Price constructor.

        Args:
            size: Price length.
        """
        self.stock_total_volume = 2000
        self.init()

    def init(
        self,
    ) -> None:
        """Initialize trading data set.
        """
        price_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "bitcoin_price.csv"))
        extra_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "bitcoin_dataset.csv"))
        price = pd.read_csv(price_file)
        price["Date"] = pd.to_datetime(price.Date)
        extra = pd.read_csv(extra_file)
        extra["Date"] = pd.to_datetime(extra.Date)

        self.price_ext = price.merge(extra, on="Date", how="left")
        self.price_ext["daily_return"] = self.price_ext["Close"].pct_change()
        self.price_ext.sort_values("Date", ascending=True, inplace=True)
        self.price_list = self.price_ext.Close.tolist()
        self.price_list_size = self.price_ext.shape[0]
