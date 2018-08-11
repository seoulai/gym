"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
from typing import Tuple
from typing import Dict
from typing import List
import numpy as np
from seoulai_gym.envs.traders.base import Constants
# from seoulai_gym.envs.checkers.base import DarkPiece
# from seoulai_gym.envs.checkers.rules import Rules


class Price(Constants):
  def __init__(
      self,
      price_list_size: int=1000,
      tick=0
  ):
    """Price constructor.

    Args:
        size: Price length.
    """
    self.stock_total_volumn = 2000
    self.price_list_size = price_list_size
    self.tick = tick
    self.init()

  def init(
      self,
  ) -> None:
    """Initialize board and setup pieces on board.
    volumn_list 거래량

    Note: Dark pieces should be ALWAYS on the top of the board.
    """
    self.price_list = np.random.rand(self.price_list_size)*100
    # self.volumn_list = np.random.rand(self.total)*100

  def conclude(
      self,
      decision,
      stock_price,
      sotck_volumn
  )-> Tuple[float, int, bool, Dict]:
    rew = 0  # TODO compute reward
    info = {}
    # current_price 로 체결이 됐다고 가정.

    # checking valid order
    if decision == 'buy' and (self.stock_total_volumn - sotck_volumn) > 0:
      self.stock_total_volumn = self.stock_total_volumn - sotck_volumn
    elif decision == 'sell':
      self.stock_total_volumn = self.stock_total_volumn + sotck_volumn

    if self.stock_total_volumn == 0:
      done = True
    else:
      done = False

    if self.tick < self.price_list_size-1:
      self.tick = self.tick + 1
    else:
      done = True

    return self.price_list[self.tick], rew, done, info
