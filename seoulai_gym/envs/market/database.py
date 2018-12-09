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

        self.others= dict(
            total_ask_size=None,
            total_bid_size=None,
            ask_bid=None,
            change_price=None,
            prev_closing_price=None,
            ap1 =None,
            bp1 =None,
            as1=None,
            bs1=None,
            ap2=None,
            bp2=None,
            as2 =None,
            bs2=None,
            ap3=None,
            bp3=None,
            as3=None,
            bs3=None,
            ap4=None,
            bp4=None,
            as4=None,
            bs4=None,
            ap5 =None,
            bp5=None,
            as5=None,
            bs5=None,
            ap6=None,
            bp6=None,
            as6=None,
            bs6=None,
            ap7=None,
            bp7=None,
            as7 =None,
            bs7=None,
            ap8=None,
            bp8=None,
            as8=None,
            bs8=None,
            ap9=None,
            bp9=None,
            as9=None,
            bs9=None,
            ap10=None,
            bp10=None,
            as10=None,
            bs10=None,
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

        self.portfolio_log= dict(
            timestamp="hh:mm:ss",
            val=100000000.0,
            mdd=0.0,
            sharp=0.0,
        )

