## Installation

install from source.

```bash
git clone -b market https://github.com/seoulai/gym.git

cd gym

pip3 install -e .
```


## Seoul AI Market Framework

Seoul AI Market is based ona real-time <a href="https://github.com/seoulai/gym">reinforcement learning</a> based method.


```python
import seoulai_gym as gym
from itertools import count
from seoulai_gym.envs.market.base import Constants

your_id = "seoul_ai"
mode = Constants.LOCAL

### Create your agent.
a1 = YourAgentClassName(
     your_id,
     )

### Create your market environment. 
env = gym.make("Market")

### Select your id and mode to participate
env.participate(your_id, mode)

### reset fetches the initial state of the crypto market.
obs = env.reset()

### Perform real-time reinforcement learning
for t in count():
    # Call act for the agent to take an action
    action = a1.act(obs)
    
    # To send your action to market:  
    obs, rewards, done, _ = env.step(**action)
    
    # We reccomend that rewards override user-defined fuctions
    a1.postprocess(obs, action, next_obs, rewards)
```

## Setup details 

### mode

- There are 2 modes: LOCAL and HACKATHON.
- Your agent will start trading in HACKATHON mode. This will affect the virtual KRW balance provided by Seoul AI.
- You can trian your agent in the LOCAL mode. We advice you to train your agent before trying out the HACKATHON mode.

#### LOCAL mode Example 1

```python
your_id = "seoul_ai"
mode = Constants.LOCAL

env = gym.make("Market")
env.participate(your_id, mode)

# IF you call reset in LOCAL, your cash and balance will be updated to 100,000,000 KRW and 0.0 respectively.
obs = env.reset()

for t in count():
    action = a1.act(obs)
    next_obs, rewards, done, _ = env.step(**action)    # action is in dictionary format.
    a1.postprocess(obs, action, next_obs, rewards)
```

#### LOCAL mode Example 2

```python
your_id = "seoul_ai"
mode = Constants.LOCAL

env = gym.make("Market")
env.participate(your_id, mode)

obs = env.reset()

# You can use Episodes under LOCAL mode to train similar scenarios.
EPISODES = 100
for e in EPISODES: 
    for t in count():
        action = a1.act(obs)
        next_obs, rewards, done, _ = env.step(**action)    # action is in dictionary format.
        a1.postprocess(obs, action, next_obs, rewards)
    
        # The game ends once the agent has been trained on all Local data
        if done:
            break
```

#### HACKATHON mode Example

```python
your_id = "seoul_ai"
mode = Constants.HACKATHON

env = gym.make("Market")
env.participate(your_id, mode)

# Calling reset in HACKATHON mode fetches the cash and balance
# It is different from calling reset in LOCAL as your cash and balance will not be reset.
obs = env.reset()


# You cannot train with Episodes in HACKATHON mode.
for t in count():
    action = a1.act(obs)
    next_obs, rewards, done, _ = env.step(**action)    # action is in dictionary format.
    a1.postprocess(obs, action, next_obs, rewards)
```

### act

```python
action = a1.act(obs)
```
The act function calls the following functions.
- _get_common() = saves raw data fetched by obs to as an agent class variable
- preprocess() = changes raw data fetched by obs to state
- algo() = performs training as defined by the participant.

    
### step
The step function fetches and saves the crypto market state so that the agent may start trading. This function returns 3 variables.

#### `obs`
obs is short for observation.
The datasets in obs are as follows:

```python
order_book = obs.get("order_book")    # [Buy price, Current price, Sell price]
statistics = obs.get("statistics")    # {Statistical value for agent's use}
agent_info = obs.get("agent_info")    # {Cash, balance amount}
portfolio_rets = obs.get("portfolio_rets")    # {Portfolio indicators based on algorithm performance}
```
#### `rewards`
There are 5 types of rewards

```python
rewards = dict(
    return_amt=return_amt,    # Revenue from current action
    return_per=return_per,    # Yield from current action (current value of portfolio/ previous value of portfolio -1) * 100(%)
    return_sign=return_sign,    # 1 if profited from current action. -1 if loss. 0 if no change. 
    score_amt=score_amt,    # Amount of revenue (or profit or loss) incurred to date relative to initial capital (10,000,0000 KRW)
    score=score)    # Revenue (or profit or loss) incurred to date relative to initial capital (110,000,0000 KRW) (%)
```

#### `done`
The value of done is always False under HACKATHON mode.


### Developing Agent class

#### Creating your agent

```python
import seoulai_gym as gym
from seoulai_gym.envs.market.agents import Agent

# Your agent must inherit from Seoul AI's agent class
class YourAgentClassName(Agent):
    ...
```

#### _get_common() function
_get_common function calls agent's act function. obs takes raw data and saves it as a variable in the agent's class.
```python
    def _get_common(
        self,
        obs,
    ):
        self.order_book = obs.get("order_book")
        self.statistics = obs.get("statistics")

        self.agent_info = obs.get("agent_info")
        self.portfolio_ret = obs.get("portfolio_rets")

        self.cash = self.agent_info["cash"]
        self.asset_qtys = self.agent_info.get("asset_qtys")    # balance amount
        self.cur_price = self.order_book[0+1]    # current price
```

#### set_actions function defition
All participants must define the set_action function.
actions must be in dictionary form and must be returned.

```python
class YourAgentClassName(Agent):

    def set_actions(
        self,
    )->dict:

        your_actions = {}

        """ 
        The dictionary's key is action name, value is order_percent.
        action name is named by the participant
        order_percent takes value between -100 and 100
        order_percent values + represents to buy and - represents to sell.
       """

        your_actions = dict(
            holding = 0,
            buy_all = +100,    # buy_all means that you will buy 100% of the purchase amount
            sell_20per = -20,  # sell_20per means buy and sell 20% of the available volume
        )
        return your_actions    # You must return the actions dictionary you defined.
```

#### preprocess
You can select your data from raw data (fetched by obs), and change it as you'd like. We encourage that you perform data normalization.

- preprocess is optional. If omitted, obs is entered as state.

```python
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
```

#### algo (algorithm definition)
It is a function that defines the conditions for tradtion.

```python
    def algo(
        self,
        state,
    ):
        if state["buy_signal"]:
            # Enter action_name as a parameter of set_actions
            return self.action("buy_all")
        elif state["sell_signal"]:
            return self.action("sell_20per")
        else:
            return self.action(0)    # You can enter the index of the action_name defined in set_actions as a parameter.
```

#### postprocess
You can redifine rewards through the postprocess.
```python
    def postprocess(
        self,
        obs,
        action,
        next_obs,
        rewards,
    ):
        your_reward = 0

        decision = action.get("decision")
        order_book = obs.get("order_book")
        cur_price = order_book[0+1]

        next_order_book = obs.get("order_book")
        next_price = next_order_book[0+1]
        diff = next_price - cur_price

        if decision == Constants.BUY and diff > 0:
            your_reward = 1
        elif decision == Constants.SELL and diff < 0:
            your_reward = 1
```

#### DQN Example
```python
# link 1
```

#### Rule based Example
<a href="https://github.com/seoulai/gym/blob/market/examples/market/mean_reverting_example.py">mean_reverting_example.py</a>
