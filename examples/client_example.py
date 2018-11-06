"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
Agent inspired by keon.io
https://keon.io/deep-q-learning/
2018
"""

import seoulai_gym as gym

from seoulai_gym.envs.market.agents import Agent 
from seoulai_gym.envs.market.base import Constants
from itertools import count


class MeanRevertingAgent(Agent):

    def define_state(
        self,
        obs,
    ):
        state = obs
        return state

    def algo(
        self,
        state,
    ):
        return 0, 0.0, 0.0    # decision, trad_qty, trad_price
    
    def define_reward(
        self,
    ):
        pass

    # TODO : prevent to define act method.
    # def act(
    #     self,
    #     obs,
    # ):
    #     state = self.define_state(obs)
    #     return self._agent_id, 0, 0.0, 0.0    # agent_id, decision, trad_qty, trad_price


if __name__ == "__main__":

    a1 = MeanRevertingAgent(
         "laplace",
         )

    env = gym.make("Market")
    obs = env.reset()
     
    # state = dict(cur_price=10000.0,
    #              ma60 = 11000.0,
    #              ma40 = 12000.0,
    #              ma20 = 10000.0,
    #              )


    for t in count():    # online RL
        action = a1.act(obs)    # local function
        next_obs, reward, done, info = env.step(Constants.LOCAL, *action)    # participants can select env_type

        if done:
            break
