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


class Market(Constants):  # , Rules):
  def __init__(
      self,
      state: str=None,
  ) -> None:
    """Initialize checkers board and its visualization.

    Args:
        state: Optional, path to saved game state. TODO

    Returns:
        None
    """
    self.price = Price()
    # self.graphics = Graphics()

  def step(
      self,
      agent,
      decision,
      stock_price: float,
      stock_volumn: int
  ) -> Tuple[List, int, bool, Dict]:
    """Make a step (= move) within board.

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

    obs, rew, done, info = self.price.conclude(
        decision, stock_price, stock_volumn)
    return copy.deepcopy(obs), rew, done, info

  def reset(
      self
  ) -> List:
    """Reset all variables and initialize new game.

    Returns:
        obs: Information about positions of pieces.
    """
    self.price = Price()
    obs = self.price.price_list
    return obs[0]

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
