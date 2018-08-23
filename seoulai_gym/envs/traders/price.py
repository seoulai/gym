"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import pandas as pd
from seoulai_gym.envs.traders.base import Constants
import os


class Price(Constants):
    def __init__(
        self,
        price_list_size: int=1000,  # trading game size
        tick: int=0,
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

        TODO: add volume, crypto networking value and etc...

        """
        price_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "bitcoin_price.csv"))
        df = pd.read_csv(price_file)
        df["Date"] = pd.to_datetime(df.Date)
        df.sort_values("Date", ascending=True, inplace=True)
        self.price_list = df.Close.tolist()
        self.price_list_size = df.shape[0]
