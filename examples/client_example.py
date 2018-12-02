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
            sell_20per = -20,
        )

        # serial define
        # your_actions = {}
        # your_actions.update( {"holding" : 0} )
        # for i in range(100):
        #     your_actions.update( {f"buy_{i+1}per": i+1} )
        # 
        # for i in range(100):
        #     your_actions.update( {f"sell_{i+1}per" : -(i+1)} )
        

        return your_actions 

    def preprocess(
        self,
        obs,
    ):
        cur_price = self.cur_price
        ma10 = self.ma[10]
        std10 = self.std[10]
        thresh_hold = 1.0

        your_state = dict(
            buy_signal=(cur_price > ma10 + std10*thresh_hold),
            sell_signal=(cur_price < ma10 - std10*thresh_hold),
        )

        return your_state 

    def algo(
        self,
        state,
    ):
        # print(state.keys())

        # return self.action(np.random.choice(range(self.action_spaces)))
        if state["buy_signal"]: 
            return self.action("buy_all")
        elif state["sell_signal"]:
            return self.action("sell_20per")
        else:
            return self.action(0)    # you can use number of index.

    def postprocess(
        self,
        obs,
        action,
        next_obs,
        rewards,
    ):

        # define reward
        your_reward = 0

        print(rewards)
        # normal reward
        your_reward = rewards.get("return_sign")

        # customized reward 1
        portfolio_rets = obs.get("portfolio_rets")
        next_portfolio_rets = next_obs.get("portfolio_rets")

        portfolio_val= portfolio_rets.get("val")
        next_portfolio_val= next_portfolio_rets.get("val")

        your_reward = portfolio_val/next_portfolio_val

        # customized reward 2
        decision = action.get("decision")
        order_book = obs.get("order_book")
        cur_price = obs.get("cur_price") 

        next_order_book = obs.get("order_book")
        next_price = obs.get("cur_price") 
        diff = next_price - cur_price

        if decision == Constants.BUY and diff > 0:
            your_reward = 1
        elif decision == Constants.SELL and diff < 0:
            your_reward = 1

        # define turn_on
        condition1 = True
        if condition1:
            self.mode = "HACKATHON"
        else:
            self.mode = "LOCAL"

        # memory
        # replay
        # other technics.


if __name__ == "__main__":

    your_id = "seoul_ai"
    mode = Constants.HACKATHON    # participants can select mode 

    a1 = MeanRevertingAgent(
         your_id,
         )

    env = gym.make("Market")
    env.participate(your_id, mode)
    obs = env.reset()

    for t in count():    # Online RL
        print(f"step {t}") 
        action = a1.act(obs)    # Local function
        next_obs, rewards, done, _= env.step(**action)
        a1.postprocess(obs, action, next_obs, rewards)

        if done:
            break

        obs = next_obs
        print(f"==========================================================================================")
