"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import numpy as np
import random
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Tuple

from seoulai_gym.envs.traders.base import Constants
# from seoulai_gym.envs.traders.rules import Rules


class Agent(ABC, Constants):
  @abstractmethod
  def __init__(
      self,
      name: str
  ):
    self._name = name

  @abstractmethod
  def act(
      self,
      obs,
      reward: int,
      done: bool,
  ) -> None:
    pass

  @property
  def name(self, _name):
    return _name

  def __str__(self):
    return self._name


class RandomAgent(Agent):
  def __init__(
      self,
      name: str
  ):
    """Initialize random agent.

    Args:
        name: name of agent.
        ptype: type of piece that agent is responsible for.
    """
    super().__init__(name)

  def act(
      self,
      obs,  # 주가, 수수료율, 현금, 자산가치
      # prices: List,  # 현재 주가
      reward: int,
      done: bool,
  ) -> Tuple[int, int, int]:
    #print("agent obs")
    # print(obs)
    """
    총 자산 = 현금 잔고 + 주식 가격 * 주식 수량
    수수료율 = 0.05%

    총 매수가 = (주식 가격 * 주식 수량) * (1 + 수수료율)
    총 매도가 = (주식 가격 * 주식 수량) * (1 + 수수료율)

    리워드 = (현재 총 자산 - 이전 총 자산) * 리워드
    종료 조건 = 파산 (총 자산 == 0)

    매도 결정 = 주식 보유 & (현재 주가 > (N일 평균 주가 - N일 주가의 표준편차))
    매수 결정 = 현금 보유 ... & (현재 주가 < (N일 평균 주가 - N일 주가의 표준편차))
    보유 결정 = 주식 보유 & ((N일 평균 주가 - N일 주가의 표준편차) < 현재 주가 < (N일 평균 주가 - N일 주가의 표준편차))

    Args:
        prices: price data set of stock.
        reward: reward for perfomed step.
        done: information about end of game.

    Returns:
        Current and new location of piece.
    """

    decision = random.choice(list(['buy', 'sell', 'hold']))
    # print(decision)
    #obs = [self.price.price_list[:10], self.cash, self.asset_val, self.balance_qty, self.fee_rt]
    price_list = obs[0]
    cash = obs[1]
    asset_val = obs[2]
    balance_qty = obs[3]
    fee_rt = obs[4]

    trad_price = price_list[-1]    # select current price
    trad_qty = 0
    max_qty = 0

    if decision == 'buy':
      fee = trad_price*fee_rt  # 수수료 계산
      # 최대 매수 가능 수량 = 보유 현금 / (주식 매수 금액 + 수수료)
      max_qty = cash/(trad_price+fee)
    elif decision == 'sell':
      max_qty = balance_qty

    if max_qty > 0:    # 최대가능수량이 0보다 클 경우 range에서 random하게 선택
      trad_qty = np.random.random_sample() * max_qty

    return decision, trad_price, trad_qty


class RandomAgentBuffett(RandomAgent):
  def __init__(
      self,
      name: str
  ):
    super().__init__(name)


class RandomAgentSon(RandomAgent):
  def __init__(
      self,
      name: str
  ):
    super().__init__(name)
