"""
Requires pytest
https://pytest.org/

James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import pytest
import seoulai_gym as gym

from seoulai_gym.envs.market.base import Constants
from seoulai_gym.envs.market.price import Price
from seoulai_gym.envs.market.agents import RandomAgent
from seoulai_gym.envs.market.market import Market
# from seoulai_gym.envs.market.board import DarkPiece
# from seoulai_gym.envs.market.board import LightPiece


@pytest.fixture
def price():
    return Price()

@pytest.fixture
def agent():
    fee_rt = 0.05/100
    return RandomAgent("test", 100000000, fee_rt)

@pytest.fixture
def market():
    env = gym.make("Market")
    fee_rt = env.select("upbit")
    return env 

class TestMarket(object):
    """Rewards should not be positive when performing invalid move.
    """

    def test_market_init(self, market):
        assert market.t == 0 
        assert market.state_size == 10 
        assert market.action_size == 3
        assert market.traders == 0

    def test_market_reset(self, market):
        obs = market.reset()
        assert market.t == 0
        assert market.max_t_size == 1000
        assert len(obs) == 1
        return obs

    def test_state_size(self, market, agent):
        obs = self.test_market_reset(market)
        # obs = market.reset()
        # assert market.t == 0
        # assert market.max_t_size == 1000 
        # assert len(obs) == 1 
        
        # first 10 step 
        obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
        assert market.t == 1 
        assert len(obs) == 2
        obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
        assert market.t == 2 
        assert len(obs) == 3
        obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
        assert market.t == 3 
        assert len(obs) == 4
        obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
        assert market.t == 4 
        assert len(obs) == 5
        obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
        assert market.t == 5 
        assert len(obs) == 6
        obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
        assert market.t == 6 
        assert len(obs) == 7
        obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
        assert market.t == 7 
        assert len(obs) == 8 
        obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
        assert market.t == 8 
        assert len(obs) == 9
        obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
        assert market.t == 9 
        assert len(obs) == 10

        # observation size should be 10
        for t in range(10, 1000):
            obs, rew, done, info = market.step(agent, Constants().HOLD, 0, 0)
            assert market.t == t
            assert len(obs) == 10
            if done:
                break

        # max t size
        assert market.t == 999 
        
    def test_cash_asset_in_action(self, market, agent):
        obs = self.test_market_reset(market)
        rew = 0
        done = False

        assert agent.cash == 100000000
        assert agent.asset_qty == 0 
        assert agent.fee_rt == 0.05/100 
        fee_rt = agent.fee_rt

        cur_price = obs[-1]
        trad_price = cur_price
        trad_qty = 1
        trading_amt = trad_price*trad_qty
        fee = trading_amt*fee_rt 

        obs, rew, done, info = market.step(agent, Constants().BUY, cur_price, 1)
        next_cash = 100000000-cur_price*1-fee
        next_qty = 0 + trad_qty
        assert agent.cash == next_cash 
        assert agent.asset_qty == next_qty 

        cur_price = obs[-1]
        trad_price = cur_price
        trad_qty = 1
        trading_amt = trad_price*trad_qty
        fee = trading_amt*fee_rt 

        obs, rew, done, info = market.step(agent, Constants().SELL, cur_price, 1)
        assert agent.cash == next_cash + trading_amt - fee
        assert agent.asset_qty == next_qty-trad_qty 

