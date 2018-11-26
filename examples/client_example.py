"""
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""

import seoulai_gym as gym
import time

from seoulai_gym.envs.market.agents import Agent
from seoulai_gym.envs.market.base import Constants
from itertools import count


class MeanRevertingAgent(Agent):

    def set_actions(
        self,
    )->dict:

        # action_spaces = 1(ticker) * 2(buy, sell) * 100(%) * (20+1)(tick) + 1(hold) = 200x21+1 = 4201

        """ 1. you must return dictionary of actions!
            row1 : action_name1 = (decision1, order_percent 1, order price 1)
            row2 : action_name2 = (decision2, order_percent 2, order price 2)
            ...

            2. If you want to add "hold" action, just define ("hold", 0, 0)
            3. order_percent = 10 means that your agent'll order 10% of possible quantity.
            
            order_price = 0 means current price.
            order_price = 10 means that your agent'll order at sell_price_10.
            order_price = -10 means that your agent'll order at buy_price_10.

            below table is order book.
            ==========================
            sell_price_10
            sell_price_9
            ...
            sell_price_1
                          buy_price_1
                          buy_price_2
                          ...
                          buy_price_10 
            ==========================
        """

        # normal define
        your_actions = {}

        your_actions = dict(
            # TODO : simplify hold
            holding=("hold", 0, 0),
            buy_all_at_cur_price=("buy", 100, 0),
            sell_20per_at_cur_price=("sell", 20, 0),
        )

        # serial define
        # your_actions = {}
        # for i in range(100):
        #     your_actions.update( {f"buy_{i+1}%_at_cur_price" : ("buy", i+1, 0)} )
        # 
        # for i in range(100):
        #     your_actions.update( {f"sell_{i+1}%_at_cur_price" : ("sell", i+1, 0)} )
        # 
        # your_actions.update( {"holding" : ("hold")} )

        return your_actions 

    def preprocess(
        self,
        obs,
    ):
        cur_price = self.cur_price
        ma10 = self.statistics.get("ma10")
        std10 = self.statistics.get("std10")
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

        if state["buy_signal"]: 
            return self.action("buy_all_at_cur_price")
        elif state["sell_signal"]:
            return self.action("sell_20per_at_cur_price")
        else:
            return self.action(0)    # participants can use number of index.

    def postprocess(
        self,
        obs,
        action,
        next_obs,
        rewards,
        done,
    ):
        # define reward
        # define turn_on
        # memory
        # replay
        # other technics.
        pass


if __name__ == "__main__":

    your_id = "seoul_ai"
    mode = Constants.LOCAL    # participants can select mode 

    a1 = MeanRevertingAgent(
         your_id,
         )

    print(f"actions_spaces = {a1.action_spaces}")
    print(f"your_action_names = {a1.action_names}")
    print(f"you can use self.common_column. common_columns = {a1._common_data_columns}")

    env = gym.make("Market")
    obs = env.reset(your_id, mode)

    for t in count():    # Online RL
        action = a1.act(obs)    # Local function
        next_obs, rewards, done, info = env.step(*action, mode)
        a1.postprocess(obs, action, next_obs, rewards, done)

        if done:
            break

        obs = next_obs
