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

from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import load_model


class DQNAgent(Agent):
    def __init__(
        self,
        agent_id: str,
    ):
        super().__init__(agent_id)
        self.state_size = 4
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.batch_size = 32

    def _build_model(
        self,
    ):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_spaces, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(
        self,
        obs,
        action,
        next_obs,
        reward,
    ):
        state = self.preprocess(obs)
        next_state = self.preprocess(next_obs)

        data = (state, action, next_state, reward)
        self.memory.append(data)

    def replay(
        self,
    ):
        minibatch = random.sample(self.memory)
        loss_history = []

        for state, action, next_state, reward in minibatch:
            target = (reward + self.gamma *
                      np.amax(self.model.predict(next_state)[0]))

            target_f = self.model.predict(state)
            index = action.get("index")
            target_f[0][index] = target
            hist = self.model.fit(state, target_f, epochs=1, verbose=0)
            loss_history.append(hist.history['loss'])

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        return loss_history

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
            buy_10per= +10,
            buy_25per= +25,
            buy_50per= +50,
            buy_100per= +100,
            sell_10per= -10,
            sell_25per= -25,
            sell_50per= -50,
            sell_100per= -100,
        )

        return your_actions 

    def preprocess(
        self,
        obs,
    ):

        # get data
        order_book = obs.get("order_book")
        trade = obs.get("trade")
        agent_info = obs.get("agent_info")
        portfolio_rets = obs.get("portfolio_rets")

        # base data
        ask_price = order_book.get("ask_price")
        bid_price = order_book.get("bid_price")
        cur_price = trade.get("cur_price")
        volume = trade.get("cur_volume")
        cash = agent_info.get("cash")
        asset_qtys = agent_info.get("asset_qtys")
        asset_qty = asset_qtys["KRW-BTC"]

        # nomalized data
        ask_per = int( (ask_price/float(cur_price))*100.0)
        bid_per = int( (bid_price/float(cur_price))*100.0)
        cash_per = int( (cash/100000000.0)*100.0)
        asset_per = int( (asset_qty/volume)*100.0)

        state = [ask_per, bid_per, cash_per, asset_per] 
        state = np.reshape(state, [1, self.state_size])

        return state

    def algo(
        self,
        state,
    ):
        # print(state.keys())

        if np.random.rand() <= self.epsilon:
            return self.action(np.random.choice(range(self.action_spaces)))
        else:
            act_values = self.model.predict(state)
            index = np.argmax(act_values[0])
            return self.action(index)

    def postprocess(
        self,
        obs,
        action,
        next_obs,
        rewards,
    ):
        # define reward
        reward = rewards.get("return_sign")

        self.remember(
            obs,
            action,
            next_obs,
            reward,
        )
        if len(self.memory) > self.batch_size:
            self.replay()


    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":

    your_id = "dqn"
    mode = Constants.LOCAL    # participants can select mode 

    a1 = DQNAgent(
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
