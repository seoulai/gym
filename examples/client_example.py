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

    def define_action(
        self,
    ):

        # action_spaces = x(ticker) * 2(buy, sell) * 100(%) * y(tick) + 1(hold) = 200xy+1
        # TODO: we should make x, y constants.
        # TODO: {key : {func1, func2, ...}} structure for pair trading.

        # normal define
        self.actions = dict(
            hold=("hold", "BTC", 0, 0),
            buy_all_at_cur_price=("buy", "BTC", 100, 0),
            sell_20per_at_cur_price=("sell", "BTC", 20, 0),)

        # serial define
        # for i in range(100):
        #     self.actions.update( {f"buy_{i+1}%_at_cur_price" : ("buy", "BTC", i+1, 0)} )
        #
        # for i in range(100):
        #     self.actions.update( {f"sell_{i+1}%_at_cur_price" : ("sell", "BTC", i+1, 0)} )
        #
        # self.actions.update( {"hold" : ("hold", "BTC", 0, 0)})

    # data preprocessing
    def define_state(
        self,
        obs,
    ):
        state = obs
        self.ma10 = obs.get("ma10")
        self.std10 = obs.get("std10")
        return state

    def algo(
        self,
        state,
    ):
        # print(state.columns)
        cur_price = self.cur_price
        ma10 = self.ma10
        std10 = self.std10
        thresh_hold = 1.0

        # TODO: dataframe structure?
        if cur_price > ma10 + std10*thresh_hold:
            return self.action("buy_all_at_cur_price")
        elif cur_price < ma10 - std10*thresh_hold:
            return self.action("sell_20per_at_cur_price")
        else:
            return self.action(0)

    def define_reward(
        self,
    ):
        pass


if __name__ == "__main__":

    a1 = MeanRevertingAgent(
         "laplace",
         )
    print(a1.action_spaces)
    print(a1.action_keys)

    env = gym.make("Market")
    obs = env.reset()

    for t in count():    # online RL
        action = a1.act(obs)    # local function
        next_obs, reward, done, info = env.step(Constants.LOCAL, *action)    # participants can select env_type

        if done:
            break
