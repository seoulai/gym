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

# import pygame
# from pygame.locals import QUIT

from seoulai_gym.envs.traders.base import Constants
from seoulai_gym.envs.traders.price import Price
# from seoulai_gym.envs.traders.graphics import Graphics
# from seoulai_gym.envs.traders.rules import Rules


class Market():
  def __init__(
      self,
      state,
  ) -> None:
    """Initialize market and its visualization.
    Args:
        state: Optional, path to saved game state. TODO

    Returns:
        None
    """
    self.reset(state)

    # graphics is for visualization
    # self.graphics = Graphics()

  def reset(
      self,
      state
  ) -> List:
    """Reset all variables and initialize new game.

    Returns:
        obs: Information about positions of pieces.
    """
    self.price = Price(state[0])    # TODO: data generator
    self.cash = state[0]    # TODO: dictionary or dataframe
    self.fee_rt = state[1]
    self.asset_qty = 0
    self.asset_val = 0
    self.tick = 0
    self.max_tick_size = 1000
    self.init_cash = self.cash

    obs = [self.price.price_list[:1], self.cash, self.asset_val, self.asset_qty, self.fee_rt]
    # TODO : obs = price + cash + asset_val, asset_qty
    return obs # reset prices data set

  def step(
      self,
      agent,
      decision,
      trad_price: float,
      trad_qty: int
  ) :
    """Make a step (= move) within market.

    Args:
        agent: Agent making a move.
        from_row: Row of board of original piece location.
        from_col: Col of board of original piece location.
        to_row: Row of board of desired piece location.
        to_col: Col of board of desired piece location.

    Returns:
        obs: Information price history.
        rew: Reward for perfomed step.
        done: Information about end of game.
        info: Additional information about current step.
    """
    # TODO: 나중에 rule에 추가
    # self.possible_moves = self.get_valid_moves(
    #     self.price.board_list, from_row, from_col)

    obs, rew, done, info = self.conclude(
        decision, trad_price, trad_qty)
    return copy.deepcopy(obs), rew, done, info
  def conclude(
        self,
        decision,
        trad_price,
        trad_qty
    )-> Tuple[float, int, bool, Dict]:
      rew = 0  # TODO compute reward
      done = False
      # daily_return? duration?

      info = {}

      # It is assumed that order is concluded as agent action.
      # in real world, it can't be possible.
      # TODO : develop backtesting logic like real world. ex. slippage
      ccld_price = trad_price    # concluded price. (체결가격)
      ccld_qty = trad_qty   # concluded quantity. (체결수량)

      trading_amt = ccld_price*ccld_qty    # total amount of moved money. (거래금액)
      fee = trading_amt*self.fee_rt    # fee(commission, 수수료)

      priv_pflo_value = self.cash+self.asset_val    # previus potfolio value(previous cash+asset_value), 이전 포트폴리오 가치(이전 현금 + 이전 자산 가치)


      if decision == 'buy':
        self.cash = self.cash-trading_amt-fee   # after buying, cash will decrease. (매수 후, 현금은 줄어든다.)
        self.asset_qty = self.asset_qty + ccld_qty    # quantity of asset will increase. (매수 후, 자산 수량은 늘어난다.)
      elif decision == 'sell':
        self.cash = self.cash+(trading_amt-fee)    # after selling, cash will increase. (매도 후, 현금은 증가한다.)
        self.asset_qty = self.asset_qty - ccld_qty    # quantity of asset will decrease. (매도 후, 자산 수량은 줄어든다.)

      cur_price = self.price.price_list[self.tick]    # current price (현재가)
      self.asset_val = self.asset_qty*cur_price    # current asset value is asset_qty x current price (현재 자산 가치 = 자산 수량 x 현재가)
      cur_pflo_value = self.cash+self.asset_val    # current potfolio value(current cash+asset_value) 현재 포트폴리오 가치(현재 현금, 현재 자산 가치)

      rew = cur_pflo_value-priv_pflo_value    # money that you earn or lose in 1 tick. (1 tick 동안의 decision으로 변화한 포트폴리오 가치를 reward로 잡음)

      # checking valid order
      # self.stock_total_volume will be discussed.
      """
      if decision == 'buy' and (self.stock_total_volume - stock_volume) > 0:
        self.stock_total_volume = self.stock_total_volume - stock_volume
      elif decision == 'sell':
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
      if self.tick >= self.max_tick_size:
        done = True

      # if you lose 20% of your money,  game over
      if ((cur_pflo_value/self.init_cash)-1)*100 < -20.0:
        done = True

      # observation = [[history of prices], cash, asset value, quantity of asset, fee_ratio]
      obs = [self.price.price_list[:self.tick], self.cash, self.asset_val, self.asset_qty, self.fee_rt]

      return obs, rew, done, info

  def render(
      self,
  ) -> None:
    """Display current state of board.

    Returns:
        None
    """
    # self.graphics.update(
    #     self.price.price_list,
    #     self.piece_location,
    #     self.possible_moves,
    # )

    # for event in pygame.event.get():
    #   if event.type == QUIT:
    #     pygame.quit()

  def close(
      self,
  ) -> None:
    pass
    # pygame.display.quit()
    # pygame.quit()
    # # pygame has to be again initialized, otherwise window does not close
    # pygame.init()
