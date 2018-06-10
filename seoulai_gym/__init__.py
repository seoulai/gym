"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
from seoulai_gym.envs.checkers.checkers import Checkers


def make(name: str):
    if name == "Checkers":
        return Checkers()
    else:
        raise ValueError("Unknown gym.")
