"""
Stock Market
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import pandas as pd
import numpy as np
import time

from seoulai_gym.envs.market.base import Constants
from seoulai_gym.envs.market.api import BaseAPI
from seoulai_gym.envs.market.base import Constants
from seoulai_gym.envs.market.crawler import DataCrawler 
from seoulai_gym.envs.market.database import DataBase 


class Market(BaseAPI):
    def __init__(
        self,
        state: str = None,
    ) -> None:
        """Initialize market and its visualization.
        Args:
            state: Optional, path to saved game state. TODO
        Returns:
            None
        """

        self.exchange = "Upbit"

    def participate(
        self,
        agent_id: str="your_id",
        mode: int=Constants.LOCAL,
    ):
        self._agent_id = agent_id
        self._mode = mode

    def reset(
        self,
    ):
        if self._mode == Constants.LOCAL:
            return self.local_reset()
        elif self._mode == Constants.HACKATHON:
            return self.api_reset()
        else:
            raise Exception("invalid mode!!! : LOCAL = 0, HACKATHON = 1")

    def local_reset(
        self,
    ):
        # initialize variables for local excution

        self.fee_rt = 0.05/100

        self.db = DataBase()

        self.crawler = DataCrawler(self.db)
        self.crawler.scrap()

        obs = dict(
            order_book=self.db.order_book,
            trade=self.db.trade,
            # statistics=self.db.statistics,
            agent_info=self.db.agent_info,
            portfolio_rets=self.db.portfolio_rets,
        )

        return obs

    def api_reset(
        self,
    ):
        """Reset all variables and initialize trading game.
        Returns:
            state: Information about trading parameters.
        """
        data = dict(exchange=self.exchange)
        r = self.api_get("select", data)
        self.fee_rt = r.get("fee_rt")

        data = dict(agent_id=self._agent_id)
        r = self.api_get("reset", data)
        obs = r.get("obs")

        return obs

    def step(
        self,
        index,
        agent_id: int,
        ticker: str,
        decision: int,
        trad_qty: float,
        trad_price: float,
    ):
        if self._mode == Constants.LOCAL:
            return self.local_step(agent_id, ticker, decision, trad_qty, trad_price) 
        elif self._mode == Constants.HACKATHON:
            return self.api_step(agent_id, ticker, decision, trad_qty, trad_price) 
        else:
            raise Exception("invalid mode!!! : LOCAL = 0, HACKATHON = 1")

    def validate_action(
        self,
        agent_id: int,
        ticker: str,
        decision: int,
        trad_qty: float,
        trad_price: float,
    ):
        return True

    def local_step(
        self,
        agent_id: int,
        ticker: str,
        decision: int,
        trad_qty: float,
        trad_price: int,
    ):

        rewards = {} 
        done = False
        info = {}

        is_valid_order = self.validate_action(agent_id, ticker, decision, trad_qty, trad_price)
        if not is_valid_order:
            # reward...
            # info...
            pass
        
        # 1. Conclude
        ccld_price, ccld_qty = self.conclude(
            agent_id, ticker, decision, trad_qty, trad_price)


        # 2. Data Select & Update
        # 2-1. Select cur_price and portfolio_rets
        cur_price = self.db.trade.get("cur_price")
        portfolio_rets = self.db.portfolio_rets
        portfolio_val = portfolio_rets.get("val")

        # 2-2. Update agent_info(Floating Point Problem)
        agent_info = self.db.agent_info
        cash = agent_info.get("cash")
        asset_qtys = agent_info.get("asset_qtys")
        asset_qty = asset_qtys[ticker]

        trading_amt = round(ccld_price*ccld_qty, 4)
        fee = round(trading_amt*self.fee_rt, 4)    # fee = trading_amt x 0.0005

        if decision == Constants.BUY:
            asset_val = round(trading_amt + fee, 4)
            cash = round(cash - asset_val, 4)    # after buying, cash will decrease.
            asset_qty = round(asset_qty + ccld_qty, 4)    # quantity of asset will increase.
            asset_qtys[ticker] = asset_qty

        elif decision == Constants.SELL:
            asset_qty = round(asset_qty - ccld_qty, 4)    # quantity of asset will decrease.
            asset_qtys[ticker] = asset_qty
            asset_val = round(trading_amt - fee, 4)
            cash = round(cash + asset_val, 4)    # after selling, cash will increase.

        self.db.agent_info["cash"] = cash
        self.db.agent_info["asset_qtys"] = asset_qtys 


        # 3. Scrapping(order book, trade, statistics)
        self.crawler.scrap()
        next_obs = dict(
            order_book=self.db.order_book,
            trade=self.db.trade,
            # statistics=self.db.statistics,
            )


        # 4. Update portfolio_rets(Floating Point Problem)
        next_price = self.db.trade.get("cur_price")
        asset_val = round(asset_qty * next_price, 4)
        next_portfolio_val = round(cash + asset_val, 4) 
        self.db.portfolio_rets["val"] = next_portfolio_val
        # TODO : df, mdd, sharp
        # df = self.db.portfolio_log


        # 5. Generate obs
        next_obs.update(dict(
            agent_info=self.db.agent_info,
            portfolio_rets=self.db.portfolio_rets,
            )
        )


        # 6. Generate rewards(Floating Point Problem)
        return_amt = round(next_portfolio_val - portfolio_val, 4)
        return_per = round(((next_portfolio_val/portfolio_val)-1.0)*100.0, 2)
        return_sign = np.sign(return_amt)
        change_price = next_price-cur_price
        change_price_sign = np.sign(change_price)
        hit = 1.0 if (decision == Constants.BUY and change_price_sign > 0) or (decision == Constants.SELL and change_price_sign < 0) else 0.0
        score_amt = round(next_portfolio_val - 100000000.0, 4)
        score = round(((next_portfolio_val/100000000.0)-1.0)*100.0, 2)

        rewards = dict(
            return_amt=return_amt,
            return_per=return_per,
            return_sign=return_sign,
            hit=hit,
            score_amt=score_amt,
            score=score,
            )

        # 7. Done
        if self.crawler.t  == len(self.crawler.data):
            done = True

        # 8. Time sleep
        time.sleep(0.3)

        return next_obs, rewards, done, info 

    def conclude(
        self,
        agent_id,
        ticker,
        decision,
        trad_qty: float,
        trad_price: int,
    ):

        # It is assumed that order is concluded as agent action.
        # in real world, it can't be possible.
        # TODO : develop backtesting logic like real world. ex. slippage
        ccld_price = int(trad_price)    # concluded price.
        ccld_qty = trad_qty   # concluded quantity.

        return ccld_price, ccld_qty

    def api_step(
        self,
        agent_id: int,
        ticker: str,
        decision: int,
        trad_qty: float,
        trad_price: float,
    ):
        """Make a step (= move) within market.
        Args:
            agent: Agent name(id)
            decision : buy, sell or hold. Agent position.
            trad_price: Price that Agent want to trade.
            trad_qty: Quantity that Agent want to trade.
        Returns:
            obs: Information of price history and fee ratio.
            rew: Reward for perfomed step.
            done: Information about end of game.
            info: Additional information about current step.
        """
        data = dict(agent_id=agent_id,
                    ticker=ticker,
                    decision=decision,
                    trad_qty=trad_qty,
                    trad_price=trad_price,
                    )
        r = self.api_post("step", data)

        next_obs = r.get("next_obs")
        rewards = r.get("rewards")
        done = r.get("done")
        info = r.get("info")

        return next_obs, rewards, done, info

    def scrap(
        self,
        start_time,
        end_time,
    ) -> None:
        data = dict(start_time=start_time,
                    end_time=end_time)
        data = self.api_get("scrap", data)
        return data 
