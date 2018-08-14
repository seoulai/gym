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
      init_cash,
      price_list_size: int=1000,    # trading game size
      tick=0
  ):
    """Price constructor.

    Args:
        size: Price length.
    """
    self.stock_total_volume = 2000
    self.price_list_size = price_list_size
    self.tick = tick
    self.init_cash = init_cash

    self.init()

  def init(
      self,
  ) -> None:
    """Initialize board and setup pieces on board.
    volume_list 거래량

    Note: Dark pieces should be ALWAYS on the top of the board.
    """
    self.price_list = np.random.rand(self.price_list_size)*100
    # self.volume_list = np.random.rand(self.total)*100

  def conclude(
      self,
      decision,
      trad_price,
      trad_qty,
      cash,
      asset_val,
      balance_qty,
      fee_rt
  )-> Tuple[float, int, bool, Dict]:
    rew = 0  # TODO compute reward
    # daily_return? duration?

    info = {}

    # Agent가 원하는대로 체결이 됐다고 가정.
    ccld_price = trad_price
    ccld_qty = trad_qty

    trading_amt = ccld_price*ccld_qty    # 거래금액
    fee = trading_amt*fee_rt

    priv_pflo_value = cash+asset_val

    if decision == 'buy':
      cash = cash-trading_amt-fee
      balance_qty = balance_qty + ccld_qty
    elif decision == 'sell':
      cash = cash+(trading_amt-fee)    # 매도 시 수수료만큼 떼고 입금
      balance_qty = balance_qty - ccld_qty

    cur_price = self.price_list[self.tick]
    asset_val = balance_qty*cur_price
    cur_pflo_value = cash+asset_val

    rew = cur_pflo_value-priv_pflo_value    # 포트폴리오 가치 변화량

    # checking valid order
    """
    if decision == 'buy' and (self.stock_total_volume - stock_volume) > 0:
      self.stock_total_volume = self.stock_total_volume - stock_volume
    elif decision == 'sell':
      self.stock_total_volume = self.stock_total_volume + stock_volume
    """

    # end of trading game?
    if self.stock_total_volume == 0:
      done = True
    else:
      done = False

    # next tick
    self.tick = self.tick + 1
    if self.tick >= self.price_list_size:
      done = True

    # -20% 미만으로 하락시 game over
    if ((cur_pflo_value/self.init_cash)-1)*100 < -20.0:
      done = True

    obs = [self.price_list[:self.tick], cash, asset_val, balance_qty, fee_rt]

    return obs, rew, done, info


