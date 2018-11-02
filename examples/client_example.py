"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
Agent inspired by keon.io 
https://keon.io/deep-q-learning/
2018
"""

import seoulai_gym as gym
import requests

from seoulai_gym.envs.market.agents import RandomAgent
from itertools import count

class TestAgent(RandomAgent):
    def __init__(
        self,
        name: str,
        init_cash,
    ):
        super().__init__(name, init_cash)

    def act(
        self,
        state,
    ):
        return 0, 0, 0    # decision, trad_qty, trad_price

if __name__ == "__main__": 
    env = gym.make("Market")
    env.select("Upbit")

    #state = env.reset()
    state = dict(cur_price=10000.0, 
                 ma60 = 11000.0,
                 ma40 = 12000.0,
                 ma20 = 10000.0,
                 )

    a1 = TestAgent(
         "Test",
         100000000.0,
         )

    hackathon_id = "laplace"
    for t in count():    # online RL
        action = a1.act(state)    # local function
        next_state, reward, done, info = env.step(hackathon_id, *action)

        if done:
            break
