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
from seoulai_gym.envs.market.dbclient import AgentInfo 


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
        data = dict(exchange=self.exchange)
        r = self.api_get("select", data)
        self.fee_rt = r.get("fee_rt")

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
        self.agent_info = AgentInfo()
        self.t = 0
        d = Data("Upbit")
        # self.data = d.tsv


        # load data
        # TODO : load local data
        # df = self.data.iloc[self.t]
        # print(df.order_book.tolist())
        # ob = self.data.order_books[0]
        # pf = self.data.portfolio_rets[0]
        # st = self.data.stats[0]
        # self.local_data = [] 

        #obs = self.data[0]
        obs = dict(
            order_book= ob,
            agent_info=dict(
                cash=100000000.0, # cash, asset_qtys
                asset_qtys={"KRW-BTC":0}
            ),
            portfolio_ret={"value":pf[0], "mdd":pf[1], "sharp":pf[2]},
            statistics={"ma10":st[0], "std10":st[1]})

        # local_data = self.data.local_data
        # obs = local_data[0]
        # obs= dict(
        #     order_book=[102.0, 102.0, 103.0],
        #     agent_info=dict(
        #         cash=100000000.0, # cash, asset_qtys
        #         asset_qtys={"KRW-BTC":0}
        #     ),
        #     portfolio_ret={"value":0, "mdd":0, "sharp":0},    # portfolio_value, max drawdown, sharp_ratio
        #     statistics=dict(
        #         ma10=105.0,
        #         std10=5.0,
        #     )
        # )    # ma10, ma20, ... , std10, std20, ...
        return obs

    def api_reset(
        self,
        agent_id: str,
    ):
        """Reset all variables and initialize trading game.
        Returns:
            state: Information about trading parameters.
        """
        data = dict(agent_id=agent_id)
        r = self.api_get("reset", data)
        obs = r.get("state")

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

        # cur_data = self.local_data[self.t]

        # current potfolio value(current cash + current asset value)
        # select_agent_info = \
        #     """ SELECT cash, asset_qtys
        #         FROM agent_info
        #         WHERE agent_id = '%s' """ % agent_id    # agent info is redis table
        # agent_info = dbclient.select(select_agent_info)
        agent_info = self.agent_info
        cash = agent_info.cash
        asset_qtys = agent_info.asset_qtys    # MAP or JSON String
        asset_qty = asset_qtys[ticker]

        # select_cur_price = \
        #     """ SELECT ccld_price
        #         FROM order_books 
        #         WHERE ticker = '%s' """ % ticker    # order_books is redis table
        # cur_price = dbclient.excute(select_cur_price)
        cur_ob = self.data.order_books[self.t]
        cur_price = cur_ob[1]    # current price (현재가)
        cur_pflo_value = cash + (asset_qty * cur_price)

        ccld_price, ccld_qty = self.conclude(
            agent_id, ticker, decision, trad_price, trad_qty)

        # Update Agent Info
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

        # update_agent_info = \
        #     """ UPDATE agent_info
        #         SET cash = %lf
        #         , asset_qtys = '%s'
        #         WHERE agent_id = '%s' """ % (cash, asset_qtys, agent_id)
        # dbclient.excute(update_agent_info)

        # update cache table
        # insert log table
        self.agent_info.cash = cash
        self.agent_info.asset_qtys = asset_qtys 

        # select_portfolio_ret = \
        #     """ SELECT mdd, sharp
        #         FROM portfolio_result
        #         WHERE agent_id = '%s' """ % agent_id 
        # portfolio_ret = dbclient.excute(select_portfolio_ret)
        # mdd = portfolio_ret.mdd
        # mdd = 0.0

        msg = ""
        # if mdd < -80.0:
        #     done = True

        if self.t >= self.max_t_size-1:
            done = True
            msg = "t overflow!! max_t_size : %d, current_t : %d " % (
                self.max_t_size, self.t)
        info["msg"] = msg

        # next t
        nt = self.t + 1
        self.t = nt
        next_ob = self.data.order_books[self.t]
        cur_price = cur_ob[1]    # current price (현재가)
        # cur_price = dbclient.excute(select_cur_price)
        next_pflo_value = cash + (asset_qty * cur_price)

        rewards = dict(
            test1=0.0,
            test2=2.0)
        # rewards = dict(
        #     1step_return_amt=(next_pflo_value-cur_pflo_value),
        #     1step_return_per=((next_pflo_value/cur_pflo_value)-1)*100,
        #     next_pflo_value=next_pflo_value,
        #     cur_pflo_value=cur_pflo_value)

        next_obs = dict(
            order_book=[102.0],
            agent_info={"cash":cash, "asset_qtys":asset_qtys},    # cash, asset_qtys
            portfolio_ret={},    # portfolio_value, mdd, sharp_ratio
            statistics=dict(
                ma10=105.0,
                std10=5.0,
            )
        )

        return next_obs, rewards, done, info

    def conclude(
        self,
        agent_id,
        ticker,
        decision,
        trad_price: float,
        trad_qty: float,
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

        next_state = r.get("next_state")
        print(next_state)
        reward = r.get("reward")
        done = r.get("done")
        info = r.get("info")

        return next_state, reward, done, info

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
