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
            timestamp=None,
            ask_price=None,
            bid_price=None,
            ask_size=None,
            bid_size=None,
        )

        self.trade = dict(
            timestamp=[],
            price=[],
            volume=[],
            ask_bid=[],
            sid=[],
        )

        self.agent_info = dict(
            cash=100000000.0,
            asset_qtys={"KRW-BTC":0.0},
        )

        self.portfolio_rets = dict(
            val=100000000.0,
            mdd=0.0,
            sharpe=0.0,
        )

        self.trade_history= dict(
            timestamp=[],
            cash=[],
            asset_qtys=[],
            val=[],
        )

