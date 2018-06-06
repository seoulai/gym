"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
from seoulai_gym.envs.checkers.checkers import Checkers
from seoulai_gym.envs.checkers import rules as checkers_rules
from seoulai_gym.envs.checkers import base as checkers_base


def make(name: str):
    available_gyms = [
        "Checkers",
    ]

    if name in available_gyms:
        return eval(f"{name}()")
    else:
        raise ValueError("Unknown gym.")
