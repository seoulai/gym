"""
Stock Market
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import pandas as pd
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

    def reset(
        self,
        agent_id: str,
        mode: int=Constants.LOCAL,
    ):
        if mode == Constants.LOCAL:
            return self.local_reset(agent_id)
        elif mode == Constants.HACKATHON:
            return self.api_reset(agent_id)
        else:
            raise Exception("invalid mode!!! : LOCAL = 0, HACKATHON = 1")

    def local_reset(
        self,
        agent_id: str,
    ):
        # initialize variables for local excution
        self.database = Data()
        obs = self.database.observe()

        return obs

    def api_reset(
        self,
        agent_id: str,
    ):
        """Reset all variables and initialize trading game.
        Returns:
            state: Information about trading parameters.
        """
        data = dict(exchange=self.exchange)
        r = self.api_get("select", data)
        self.fee_rt = r.get("fee_rt")

        data = dict(agent_id=agent_id)
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
        mode: int=Constants.LOCAL,
    ):
        if mode == Constants.LOCAL:
            return self.local_step(agent_id, ticker, decision, trad_qty, trad_price) 
        elif mode == Constants.HACKATHON:
            return self.api_step(agent_id, ticker, decision, trad_qty, trad_price) 
        else:
            raise Exception("invalid mode!!! : LOCAL = 0, HACKATHON = 1")

    def local_step(
        self,
        agent_id: int,
        ticker: str,
        decision: int,
        trad_qty: float,
        trad_price: float,
    ):
        # TODO : reward can be changed. ex. daily return, duration of winning.
        rewards = {} 
        done = False
        info = {}

        ccld_price, ccld_qty = self.conclude(
            agent_id, ticker, decision, trad_qty, trad_price)

        # SELECT * FROM agent_info WHERE agent_id = 'seoul_ai' -> result table
        # OR SELECT * FROM agent_info_log WHERE agent_id = 'seoul_ai' LIMIT 1 -> log_table
        agent_info = self.database.agent_info
        cash = agent_info.cash
        asset_qtys = agent_info.asset_qtys    # MAP or JSON String
        asset_qty = asset_qtys[ticker]
        # cur_portfolio_val = agent_info.portfolio_val

        # UPDATE agent_info
        trading_amt = ccld_price*ccld_qty
        fee = trading_amt*self.fee_rt
        if decision == Constants.BUY:
            cash = cash-trading_amt-fee    # after buying, cash will decrease.
            asset_qty = asset_qty + ccld_qty    # quantity of asset will increase.
            asset_qtys[ticker] = asset_qty
        elif decision == Constants.SELL:
            cash = cash+(trading_amt-fee)    # after selling, cash will increase.
            asset_qty = asset_qty - ccld_qty    # quantity of asset will decrease.
            asset_qtys[ticker] = asset_qty
        self.database.agent_info.cash = cash
        self.database.agent_info.asset_qtys = asset_qtys 

        next_obs = self.database.observe()    # next_obs is based on current time.

        msg = ""
        # if mdd < -80.0:
        #     done = True

        # if self.t >= self.max_t_size-1:
        #     done = True
        #     msg = "t overflow!! max_t_size : %d, current_t : %d " % (
        #         self.max_t_size, self.t)
        # info["msg"] = msg

        rewards = dict(
            test1=0.0,
            test2=2.0)
        # rewards = dict(
        #     1step_return_amt=(next_pflo_value-cur_pflo_value),
        #     1step_return_per=((next_pflo_value/cur_pflo_value)-1)*100,
        #     next_pflo_value=next_pflo_value,
        #     cur_pflo_value=cur_pflo_value)

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
        print(next_obs)
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
