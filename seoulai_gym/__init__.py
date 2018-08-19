"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
from seoulai_gym.envs.checkers.checkers import Checkers
from seoulai_gym.envs.traders.market import Market


def make(name: str):
  if name == "Checkers":
    return Checkers()
  elif name == "Market":
    return Market()
  else:
    raise ValueError("Unknown gym.")
