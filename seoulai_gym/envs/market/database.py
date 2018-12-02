"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""

class DataBase():
    def __init__(
        self,
    ):

        # Table Schema

        self.order_book = dict(
            ask_price=None,
            bid_price=None,
            ask_size=None,
            bid_size=None,
        )

        self.trade = dict(
            cur_price=None,
            cur_volume=None,
        )

        self.statistics = dict(
            macd_first=None,
            macd_second=None,
            macd_third=None,
            stoch_first=None,
            stoch_second=None,
            ma=None,
            sma=None,
            rsi=None,
            std=None,
        )

        self.agent_info = dict(
            cash=100000000.0,
            asset_qtys={"KRW-BTC":0.0},
        )

        self.portfolio_rets = dict(
            val=100000000.0,
            mdd=0.0,
            sharp=0.0,
        )

