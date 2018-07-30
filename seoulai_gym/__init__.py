"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
from seoulai_gym.envs.checkers.checkers import Checkers
from seoulai_gym.envs.mighty.mighty import Mighty

def make(name: str):
    if name == "Checkers":
        return Checkers()
    elif name == "Mighty":
        return Mighty()
    else:
        raise ValueError("Unknown gym.")
