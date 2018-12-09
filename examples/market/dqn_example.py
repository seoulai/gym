"""
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""

import seoulai_gym as gym
import numpy as np
import random
import logging

from seoulai_gym.envs.market.agents import Agent
from seoulai_gym.envs.market.base import Constants
from itertools import count

from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import load_model

logging.basicConfig(level=logging.INFO)

class DQNAgent(Agent):
    def __init__(
        self,
        agent_id: str,
    ):
        super().__init__(agent_id)
        self.state_size = 2
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.batch_size = 32
        self.win_cnt = 0

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
        minibatch = random.sample(self.memory, self.batch_size)
        loss_history = []

        for state, action, next_state, reward in minibatch:
            target = (reward + self.gamma *
                      np.amax(self.model.predict(next_state)[0]))

            target_f = self.model.predict(state)
            index = action.get("index")
            target_f[0][index] = target
            hist = self.model.fit(state, target_f, epochs=1, verbose=0)
            loss_history.append(hist.history['loss'])

        logging.info(f"EPSILON {self.epsilon}")
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        return loss_history

    def set_actions(
        self,
    )->dict:

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

        your_actions = {}

        # self.action_spaces = 9
        your_actions = dict(
            holding = 0,
            buy_10per = (+10, '%'),
            buy_25per = (+25, '%'),
            buy_50per = (+50, '%'),
            buy_100per = (+100, '%'),
            sell_10per = (-10, '%'),
            sell_25per = (-25, '%'),
            sell_50per = (-50, '%'),
            sell_100per = (-100, '%'),
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
        volume = trade.get("volume")
        cash = agent_info.get("cash")
        asset_qtys = agent_info.get("asset_qtys")
        asset_qty = asset_qtys["KRW-BTC"]
        asset_val = round(asset_qty*cur_price, 4)
        gap = abs(ask_price-bid_price)
        pred_fee = round(cur_price*self.fee_rt, 4)
        portfolio_val = portfolio_rets.get("val")

        # nomalized data        
        cash_ratio = round(cash/portfolio_val, 2)
        # asset_per = round(asset_val/portfolio_val, 2)
        gap_per = round(gap/pred_fee-1, 2)
        # asset_ratio = round(asset_val/cash, 2)

        state = [cash_ratio, gap_per] 
        state = np.reshape(state, [1, self.state_size])

        return state

    def algo(
        self,
        state,
    ):
        # print(state.keys())

        logging.info(f"STATE {state}")

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
        reward = rewards.get("hit")
        self.win_cnt += reward

        self.remember(obs, action, next_obs, reward)

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
        logging.info(f"step {t}")

        # Logging current observation
        order_book = obs.get("order_book")
        trade = obs.get("trade")
        agent_info = obs.get("agent_info")
        portfolio_rets = obs.get("portfolio_rets")

        logging.info(f"ORDER_BOOK {order_book}")
        logging.info(f"TRADE {trade}")
        logging.info(f"AGENT_INFO {agent_info}")
        logging.info(f"PORTFOLIO_RETS {portfolio_rets}")

        action = a1.act(obs)    # Local function
        next_obs, rewards, done, _= env.step(**action)
        a1.postprocess(obs, action, next_obs, rewards)

        # Logging action and rewards
        logging.info(f"ACTION {action}")
        logging.info(f"REWARDS {rewards}")

        # Win ratio
        win_ratio =  round( (a1.win_cnt/float(t+1))*100, 2)
        logging.info(f"WIN_RATIO {win_ratio}")

        # Logging next observation
        next_order_book = next_obs.get("order_book")
        next_trade = next_obs.get("trade")
        agent_info = next_obs.get("agent_info")
        portfolio_rets = next_obs.get("portfolio_rets")
        logging.info(f"NEXT ORDER_BOOK {next_order_book}")
        logging.info(f"NEXT TRADE {next_trade}")
        logging.info(f"NEXT AGENT_INFO {agent_info}")
        logging.info(f"NEXT PORTFOLIO_RETS {portfolio_rets}")

        if done:
            break

        obs = next_obs
        logging.info(f"==========================================================================================")
