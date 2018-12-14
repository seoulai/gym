"""
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""

import seoulai_gym as gym
import numpy as np
import time

from seoulai_gym.envs.market.agents import Agent
from seoulai_gym.envs.market.base import Constants
from itertools import count


class MeanRevertingAgent(Agent):

    def preprocess(
        self,
        obs,
    ):
        # get data
        trades = obs.get("trade")
        cur_price = trades["price"][0]

        n = 100
        price_n= trades["price"][:n]

        ma = np.mean(price_n)
        std = np.std(price_n)
        thresh_hold = 1.0

        your_state = dict(
            buy_signal=(cur_price > ma + std * thresh_hold),
            sell_signal=(cur_price < ma - std * thresh_hold),
        )

        return your_state 

    def algo(
        self,
        state,
    ):
        # print(state.keys())
        print(state["buy_signal"], state["sell_signal"])

        if state["buy_signal"]: 
            return self.action("buy_0_1")
        elif state["sell_signal"]:
            return self.action("sell_0_1")
        else:
            return self.action(0)    # you can use number of index.

    def postprocess(
        self,
        obs,
        action,
        next_obs,
        rewards,
    ):
        pass 


if __name__ == "__main__":

    your_id = "mean_reverting"
    mode = Constants.TEST    # participants can select mode 

    """ 1. You must define dictionary of actions! (key = action_name, value = order_parameters)
        
        your_actions = dict(
            action_name1 = order_parameters 1,
            action_name2 = order_parameters 2,
            ...
        )

        2. Order parameters
        order_parameters = +10 It means that your agent'll buy 10 bitcoins.
        order_parameters = -20 It means that your agent'll sell 20 bitcoins.

        order_parameters = (+10, '%') It means buying 10% of the available amount.
        order_parameters = (-20, '%') It  means selling 20% of the available amount.

        3. If you want to add "hold" action, just define "your_hold_action_name = 0"

        4. You must return dictionary of actions.
    """

    your_actions = dict(
        holding = 0,
        buy_0_1= +0.1,
        sell_0_1 = -0.1,
    )

    a1 = MeanRevertingAgent(
         your_id,
         your_actions,
         )

    env = gym.make("Market")
    env.participate(your_id, mode)
    obs = env.reset()

    for t in count():    # Online RL
        print(f"step {t}") 

        action = a1.act(obs)    # Local function
        next_obs, rewards, done, _= env.step(**action)
        a1.postprocess(obs, action, next_obs, rewards)
        print("ACTION", action)
        print("REWARDS", rewards)

        if done:
            break

        obs = next_obs
        print(f"==========================================================================================")
