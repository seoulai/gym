"""
Stock Market
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import copy
from typing import Dict
from typing import List
from typing import Tuple

import pygame
from pygame.locals import QUIT

from seoulai_gym.envs.traders.base import Constants
from seoulai_gym.envs.traders.price import Price
from seoulai_gym.envs.traders.graphics import Graphics


class Market():
    def __init__(
        self,
        state: str=None,
    ) -> None:
        """Initialize market and its visualization.
        Args:
            state: Optional, path to saved game state. TODO
        Returns:
            None
        """
        self.init()

        # graphics is for visualization
        self.graphics = Graphics()

    def init(
        self,
    ):
        self.price = Price()    # TODO: data generator
        self.tick = 0
        self.max_tick_size = 1000

    def select(
        self,
        exchang_name: str,
    ):

        # TODO : add some exchanges. ex. bithumb, bittrex, coinone, binance...
        # TODO : fixed parameters(fee ratio...) can't be edited.
        if exchang_name == "upbit":
            self.fee_rt = 0.05/100
        else:
            self.fee_rt = 0.10/100

    def reset(
        self
    ) -> List:
        """Reset all variables and initialize new game.
        Returns:
            obs: Information about trading parameters.
        """

        self.init()

        obs = [self.price.price_list[:1], self.fee_rt]
        return obs

    def step(
        self,
        agent,
        decision,
        trad_price: float,
        trad_qty: int,
    ):
        """Make a step (= move) within market.
        Args:
            agent: Agent making a decision(buy, sell and hold).
            decision : buy, sell or hold. Agent position.
            trad_price: Price that Agent want to trade.
            trad_qty: Quantity that Agent want to trade.
        Returns:
            obs: Information of price history and fee ratio.
            rew: Reward for perfomed step.
            done: Information about end of game.
            info: Additional information about current step.
        """

        obs, rew, done, info = self.conclude(
            agent, decision, trad_price, trad_qty)
        return copy.deepcopy(obs), rew, done, info

    def conclude(
        self,
        agent,
        decision,
        trad_price: float,
        trad_qty: int,
    )-> Tuple[float, int, bool, Dict]:
        
        # TODO : reward can be changed. ex. daily return, duration of winning.
        rew = 0
        done = False
        

        info = {}

        # It is assumed that order is concluded as agent action.
        # in real world, it can't be possible.
        # TODO : develop backtesting logic like real world. ex. slippage
        # TODO : add tax ratio and calculate tax. but crypto currency tax don't exist for now.
        ccld_price = trad_price    # concluded price. (체결가격)
        ccld_qty = trad_qty   # concluded quantity. (체결수량)

        # total amount of moved money. (거래금액)
        trading_amt = ccld_price*ccld_qty
        fee = trading_amt*self.fee_rt    # fee(commission, 수수료)

        # previus potfolio value(previous cash+asset_value), 이전 포트폴리오 가치(이전 현금 + 이전 자산 가치)
        priv_pflo_value = agent.cash+agent.asset_val

        if decision == Constants.BUY:
            # after buying, cash will decrease. (매수 후, 현금은 줄어든다.)
            agent.cash = agent.cash-trading_amt-fee
            # quantity of asset will increase. (매수 후, 자산 수량은 늘어난다.)
            agent.asset_qty = agent.asset_qty + ccld_qty
        elif decision == Constants.SELL:
            # after selling, cash will increase. (매도 후, 현금은 증가한다.)
            agent.cash = agent.cash+(trading_amt-fee)
            # quantity of asset will decrease. (매도 후, 자산 수량은 줄어든다.)
            agent.asset_qty = agent.asset_qty - ccld_qty

        cur_price = self.price.price_list[self.tick]    # current price (현재가)
        # current asset value is asset_qty x current price (현재 자산 가치 = 자산 수량 x 현재가)
        agent.asset_val = agent.asset_qty*cur_price
        # current potfolio value(current cash+asset_value) 현재 포트폴리오 가치(현재 현금, 현재 자산 가치)
        cur_pflo_value = agent.cash+agent.asset_val

        # money that you earn or lose in 1 tick. (1 tick 동안의 decision으로 변화한 포트폴리오 가치를 reward로 잡음)
        rew = cur_pflo_value-priv_pflo_value

        # checking valid order
        # self.stock_total_volume will be discussed.
        """
        if decision == Constants.BUY and (self.stock_total_volume - stock_volume) > 0:
            self.stock_total_volume = self.stock_total_volume - stock_volume
        elif decision == Constants.SELL:
            self.stock_total_volume = self.stock_total_volume + stock_volume
        """

        """
        if self.stock_total_volume == 0:
            done = True
        else:
            done = False
        """

        # next tick
        self.tick = self.tick + 1

        # end of trading game?
        msg = ""
        if self.tick >= self.max_tick_size:
            done = True
            msg = "tick overflow!! max_tick_size : %d, current_tick : %d " % (
                self.max_tick_size, self.tick)

        # if you lose 20% of your money,  game over
        if ((cur_pflo_value/agent.init_cash)-1)*100 < -20.0:
            done = True
            msg = "you lose 20percent of your money!!!"

        # if you earned 20% of your money,  game over
        if ((cur_pflo_value/agent.init_cash)-1)*100 > 20.0:
            done = True
            msg = "you earned 20percent of your money!!!"

        obs = [self.price.price_list[:self.tick], self.fee_rt]

        info['priv_pflo_value'] = priv_pflo_value
        info['cur_pflo_value'] = cur_pflo_value
        info['1tick_return'] = cur_pflo_value-priv_pflo_value
        info['1tick_ret_ratio'] = ((cur_pflo_value/priv_pflo_value)-1)*100
        info['fee'] = fee
        info['portfolio_value'] = cur_pflo_value
        info['msg'] = msg

        return obs, rew, done, info

    def render(
        self,
        wallet,
        decision,
    ) -> None:
        """Display current state of board.
        Returns:
            None
        """

        self.graphics.update(
            self.price.price_list[:self.tick],
            wallet,
            decision,
        )

        for event in pygame.event.get():
            if event.type == QUIT:
                # self.graphics.quit()
                pygame.quit()

    def close(
        self,
    ) -> None:
        # self.graphics.quit()
        pygame.display.quit()
        pygame.quit()
        # pygame has to be again initialized, otherwise window does not close
        pygame.init()
