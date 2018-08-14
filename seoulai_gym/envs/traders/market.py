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
    self.balance_qty = 0
    self.asset_val = 0
    self.tick = 0
    self.max_tick_size = 1000
    self.init_cash = self.cash

    obs = [self.price.price_list[:1], self.cash, self.asset_val, self.balance_qty, self.fee_rt]
    # TODO : obs = price + cash + asset_val, balance_qty
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

      # Agent가 원하는대로 체결이 됐다고 가정.
      ccld_price = trad_price
      ccld_qty = trad_qty

      trading_amt = ccld_price*ccld_qty    # 거래금액
      fee = trading_amt*self.fee_rt

      priv_pflo_value = self.cash+self.asset_val

      if decision == 'buy':
        self.cash = self.cash-trading_amt-fee
        self.balance_qty = self.balance_qty + ccld_qty
      elif decision == 'sell':
        self.cash = self.cash+(trading_amt-fee)    # 매도 시 수수료만큼 떼고 입금
        self.balance_qty = self.balance_qty - ccld_qty

      cur_price = self.price.price_list[self.tick]
      self.asset_val = self.balance_qty*cur_price
      cur_pflo_value = self.cash+self.asset_val

      rew = cur_pflo_value-priv_pflo_value    # 포트폴리오 가치 변화량

      # checking valid order
      """
      if decision == 'buy' and (self.stock_total_volume - stock_volume) > 0:
        self.stock_total_volume = self.stock_total_volume - stock_volume
      elif decision == 'sell':
        self.stock_total_volume = self.stock_total_volume + stock_volume
      """

      # end of trading game?
      """
      if self.stock_total_volume == 0:
        done = True
      else:
        done = False
      """

      # next tick
      self.tick = self.tick + 1
      if self.tick >= self.max_tick_size:
        done = True

      # -20% 미만으로 하락시 game over
      if ((cur_pflo_value/self.init_cash)-1)*100 < -20.0:
        done = True

      obs = [self.price.price_list[:self.tick], self.cash, self.asset_val, self.balance_qty, self.fee_rt]

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
