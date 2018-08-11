"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
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
      name: str,
      wallet: float
  ):
    self._name = name
    self._wallet = wallet

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
      name: str,
      wallet: float
      # ptype: int,
  ):
    """Initialize random agent.

    Args:
        name: name of agent.
        ptype: type of piece that agent is responsible for.
    """
    super().__init__(name, wallet)  # , ptype)

  def act(
      self,
      current_price: float,  # 현재 주가
      reward: int,
      done: bool,
  ) -> Tuple[int, int, int, int]:
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
        current_price: current price of stock.
        reward: reward for perfomed step.
        done: information about end of game.

    Returns:
        Current and new location of piece.
    """

    decision = random.choice(list(['buy', 'sell', 'hold']))
    stock_price, stock_vol = random.choice([(current_price, 1)])
    # TODO: wallet에 반영
    return decision, stock_price, stock_vol


class RandomAgentBuffett(RandomAgent):
  def __init__(
      self,
      name: str,
      wallet: float
  ):
    super().__init__(name, wallet)  # , Constants().LIGHT)


class RandomAgentSon(RandomAgent):
  def __init__(
      self,
      name: str,
      wallet: float
  ):
    super().__init__(name, wallet)  # , Constants().DARK)
