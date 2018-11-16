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

    def define_action(
        self,
    )->dict:

        # action_spaces = 1(ticker) * 2(buy, sell) * 100(%) * (20+1)(tick) + 1(hold) = 200x21+1 = 4201
        # TODO: {key : {func1, func2, ...}} structure for pair trading.

        """ you must return actions dictionary!
            row1 : action_name1 = (decision1, order_percent 1, tick 1)
            row2 : action_name2 = (decision2, order_percent 2, tick 2)
            ...

            If you want to add "hold" action, you just define action_name.
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
        cur_price = self.order_book[0]
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
            return self.action(0)

    def postprocess(
        self,
        obs,
        action,
        next_obs,
        rewards,
        done,
    ):
        pass


if __name__ == "__main__":

    a1 = MeanRevertingAgent(
         "laplace",
         )
    mode = Constants.LOCAL

    print(f"actions_spaces = {a1.action_spaces}")
    print(f"your_action_names = {a1.action_names}")
    print(f"you can use self.common_column. common_columns = {a1._common_data_columns}")

    env = gym.make("Market")
    obs = env.reset(mode)

    for t in count():    # Online RL
        action = a1.act(obs)    # Local function
        next_obs, rewards, done, info = env.step(mode, *action)    # participants can select env_type
        a1.postprocess(obs, action, next_obs, rewards, done)
        time.sleep(0.1)

        if done:
            break

        obs = next_obs
