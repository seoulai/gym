"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import seoulai_gym as gym
import pandas as pd
import numpy as np
import random 
from seoulai_gym.envs.market.base import Constants 
from seoulai_gym.envs.market.agents import RandomAgent
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

COLUMN_LIST = ['decision', 'trad_price', 'trad_qty', 'cash', 'asset_qty', 'portfolio_value', 'fee', '1t_return', '1t_ret_ratio']

class DQNAgent(RandomAgent):
    def __init__(
        self,
        name: str,
        init_cash: float,
        fee_rt: float,
        state_size: int,
        action_size: int,
    ):
        super().__init__(name, init_cash, fee_rt)
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        # skip remember
        if len(state) < self.state_size or len(next_state) < self.state_size:
            return
        state = np.reshape(state, [1, self.state_size])    # https://stackoverflow.com/questions/22053050/difference-between-numpy-array-shape-r-1-and-r
        next_state = np.reshape(next_state, [1, self.state_size])    # https://stackoverflow.com/questions/22053050/difference-between-numpy-array-shape-r-1-and-r

        self.memory.append((state, action, reward, next_state, done))

    def act(self, obs, reward, done):

        price_list = obs

        # next t
        self.t = self.t + 1 

        # you should wait to accumulate data because of input state_size 
        if self.t < self.state_size:
            return Constants.HOLD, 0, 0
  
        # process of making action : decision -> trad_price -> trad_qty  
        if np.random.rand() <= self.epsilon:
            decision = random.randrange(self.action_size) #, trad_price, trad_qty
        else:
            state = np.reshape(obs, [1, state_size])    # https://stackoverflow.com/questions/22053050/difference-between-numpy-array-shape-r-1-and-r
            act_values = self.model.predict(state)
            decision = np.argmax(act_values[0])

        trad_price = price_list[-1]    # select current price
        trad_qty = 0

        # caculate max_qty 
        max_qty = self.calc_max_qty(decision, trad_price)

        # if max_qty >0 (you can trade), choose trading_qty randomly (0.0~max_qty)
        if max_qty > 0:
            trad_qty = np.random.random_sample() * max_qty
        else:
            # if max_qty = 0(you can't trade), you can't buy or sell.
            decision = Constants.HOLD
        
        self.record_bah(decision, trad_price) 
        self.record_wallet()
        
        return decision, trad_price, trad_qty  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))

            target_f = self.model.predict(state)
            target_f[0][action]= target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":

    # make Market enviroment
    env = gym.make("Market")

    # select exchange
    # TODO: add trading condition of real exchanges.
    # then users will be able to choose exchange.
    fee_rt = env.select("upbit")

    state_size = env.state_size    # env.observation_space.shape[0]
    action_size = env.action_size    # env.action_space.n
    batch_size = 32
    init_cash = 100000000  # KRW
    
    a1 = DQNAgent("DQN", init_cash, fee_rt, state_size, action_size)
    current_agent = a1

    episodes = 10
    time_series_size = 1000
    

    # iterate trading simulation
    for e in range(episodes):
        # reset env
        obs = env.reset()
        # reset agent condition(cash, asset_qty)
        current_agent.init()
        rew = 0
        done = False
        
        print("episode : %d"%e)
        print("cash : %lf, asset_val : %lf"%(current_agent.cash, current_agent.asset_val))

        record = pd.DataFrame(columns = COLUMN_LIST) 
       
        for t in range(time_series_size):
            decision, trad_price, trad_qty = current_agent.act(obs, rew, done)
            # action_space = combination of [decision, trad_price, trad_qty]
            next_obs, rew, done, info = env.step(
                current_agent, decision, trad_price, trad_qty)
            # rew = rew if not done else -10
            current_agent.remember(obs, decision, rew, next_obs, done)
            obs = next_obs
            # env.render(current_agent, info, Constants.DECISION[decision])
            
            record.loc[t] = \
                [Constants.DECISION[decision], trad_price, trad_qty \
                , current_agent.cash, current_agent.asset_qty \
                , info['cur_pflo_value'], info['fee'], info['1t_return'], info['1t_ret_ratio']]

            if done:
                wallet = current_agent.cash+current_agent.asset_val
                diff = wallet-init_cash
                print("game over!!! " + info["msg"])
                print("total result. Agent wallet: % f, Agent total_return: % f, Agent total_ret_ratio : %f" %
                      (wallet, diff, ((wallet/init_cash)-1)*100))
                # initialize agent 
                current_agent.init() 
                break
            if len(current_agent.memory) > batch_size:
                current_agent.replay(batch_size)
        # logging
        print(record)
        print(record.describe())
            #env.close()
