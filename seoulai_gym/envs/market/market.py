"""
Stock Market
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import pandas as pd
import numpy as np

from seoulai_gym.envs.market.base import Constants
from seoulai_gym.envs.market.api import BaseAPI
from seoulai_gym.envs.market.base import Constants
from seoulai_gym.envs.market.data import Data 


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
        self.fee_rt = 0.05/100

        # graphics is for visualization
        # self.graphics = Graphics()
        # self.pause = False


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
        self.database = Data()
        obs = self.database.observe()

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
        # TODO : reward can be changed. ex. daily return, duration of winning.
        rewards = {} 
        done = False
        info = {}


        is_valid_order = self.validate_action(agent_id, ticker, decision, trad_qty, trad_price)
        if not is_valid_order:
            # reward...
            # info...
            pass
        
        is_concluded, ccld_price, ccld_qty = self.conclude(
            agent_id, ticker, decision, trad_qty, trad_price)

        # SELECT portfolio_val FROM portfolio_rets WHERE agent_id = 'seoul_ai'
        portfolio_rets = self.database.portfolio_rets
        portfolio_val = portfolio_rets.get("val")

        # TODO : order cancel
        if not is_concluded:
            # order_cancel()
            pass
        else:
            # server-side don't need to execute select query. just execute below UPDATE agent_info
            agent_info = self.database.agent_info
            cash = agent_info.get("cash")
            asset_qtys = agent_info.get("asset_qtys")
            asset_qty = asset_qtys[ticker]

            # UPDATE agent_info
            BASE = Constants.BASE
            FEE_BASE = Constants.FEE_BASE

            trading_amt0 = int(ccld_price*ccld_qty*BASE)
            fee_rt0 = int(self.fee_rt*FEE_BASE)
            fee0 = int((trading_amt0*fee_rt0)/FEE_BASE)
            cash0 = int(cash*BASE)
            asset_qty0 = int(asset_qty*BASE)
            ccld_qty0 = int(ccld_qty*BASE)

            if decision == Constants.BUY:
                cash = (cash0-trading_amt0-fee0)/BASE    # after buying, cash will decrease.
                asset_qty = (asset_qty0 + ccld_qty0)/BASE    # quantity of asset will increase.
                asset_qtys[ticker] = asset_qty
            elif decision == Constants.SELL:
                cash = (cash0-trading_amt0-fee0)/BASE    # after selling, cash will increase.
                asset_qty = (asset_qty0 - ccld_qty0)/BASE    # quantity of asset will decrease.
                asset_qtys[ticker] = asset_qty
            self.database.agent_info["cash"] = cash
            self.database.agent_info["asset_qtys"] = asset_qtys 

        next_obs = self.database.observe()    # next_obs is based on current time.

        portfolio_rets = self.database.portfolio_rets
        next_portfolio_val = portfolio_rets.get("val")

        portfolio_val0 = int(portfolio_val*BASE)
        next_portfolio_val0 = int(next_portfolio_val*BASE)
        
        return_amt = (next_portfolio_val0 - portfolio_val0)/BASE
        return_per = int((next_portfolio_val0/float(portfolio_val0)-1)*100*100)/100.0
        return_sign = np.sign(return_amt)
        score_amt = (next_portfolio_val0 - 100_000_000*BASE)/BASE
        score= int((next_portfolio_val0/float(100_000_000*BASE)-1)*100*100)/100.0

        rewards = dict(
            return_amt=return_amt,
            return_per=return_per,
            return_sign=return_sign,
            score_amt=score_amt,
            score=score)

        return next_obs, rewards, done, info 

    def conclude(
        self,
        agent_id,
        ticker,
        decision,
        trad_qty: float,
        trad_price: float,
    ):

        # It is assumed that order is concluded as agent action.
        # in real world, it can't be possible.
        # TODO : develop backtesting logic like real world. ex. slippage
        ccld_price = trad_price    # concluded price.
        ccld_qty = trad_qty   # concluded quantity.

        return True, ccld_price, ccld_qty

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
        reward = r.get("reward")
        done = r.get("done")
        info = r.get("info")

        return next_obs, reward, done, info

    def scrap(
        self,
        start_time,
        end_time,
    ) -> None:
        data = dict(start_time=start_time,
                    end_time=end_time)
        data = self.api_get("scrap", data)
        return data 

    def render(
        self,
        agent,
        info,
        decision,
    ) -> None:
        """Display current state of board.
        Returns:
            None
        """
        pass

    def paused(self):
        pass

    def close(
        self,
    ) -> None:
        pass
