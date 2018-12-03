"""
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""

import sys
import seoulai_gym as gym
import numpy as np
import time

from seoulai_gym.envs.market.agents import Agent
from seoulai_gym.envs.market.base import Constants
from itertools import count


class RandomAgent(Agent):

    def set_actions(
        self,
    )->dict:

        # action_spaces = 1(ticker) * 2(buy, sell) * 100(%) + 1(hold) = 200+1 = 201

        """ 1. you must return dictionary of actions!
            row1 : action_name1 = order_percent 1
            row2 : action_name2 = order_percent 2
            ...

            2. If you want to add "hold" action, just define "your_hold_action_name = 0"
            3. order_percent = +10 means that your agent'll buy 10% of possible quantity.
               order_percent = -20 means that your agent'll sell 20% of possible quantity.
            
        """

        # normal define
        your_actions = {}

        your_actions = dict(
            holding = 0,
            buy_all = +100,
            sell_all= -100,
        )

        return your_actions 

    def algo(
        self,
        state,
    ):
        # print(state.keys())

        return self.action(np.random.choice(range(self.action_spaces)))

    def postprocess(
        self,
        obs,
        action,
        next_obs,
        rewards,
    ):
        pass

if __name__ == "__main__":

    your_id = "random"
    mode = Constants.LOCAL    # participants can select mode 

    a1 = RandomAgent(
         your_id,
         )

    env = gym.make("Market")
    env.participate(your_id, mode)
    obs = env.reset()

    for t in count():    # Online RL
        print(f"step {t}") 
        print("ORDER_BOOK", obs.get("order_book"))
        print("TRADE", obs.get("trade"))
        print("STATISTICS", obs.get("statistics"))
        print("AGENT_INFO", obs.get("agent_info"))
        print("PORTFOLIO_RETS", obs.get("portfolio_rets"))

        action = a1.act(obs)    # Local function
        next_obs, rewards, done, _= env.step(**action)
        a1.postprocess(obs, action, next_obs, rewards)

        print("ACTION", action)
        print("REWARDS", rewards)

        if done:
            break

        obs = next_obs
        print(f"==========================================================================================")
