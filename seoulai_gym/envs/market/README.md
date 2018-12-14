## Installation

install from source.

```bash
virtualenv -p python3.6 your_virtual_env
source your_virtual_env/bin/activate

git clone -b market https://github.com/seoulai/gym.git

cd gym

pip3 install -e .
```


## Seoul AI Market Framework

Seoul AI Market is based on a real-time <a href="https://en.wikipedia.org/wiki/Reinforcement_learning">reinforcement learning</a>.


```python
import seoulai_gym as gym
from itertools import count
from seoulai_gym.envs.market.agents import Agent
from seoulai_gym.envs.market.base import Constants

class YourAgentClassName(Agent):
...

if __name__ == "__main__":
    your_id = "seoul_ai"
    mode = Constants.TEST

    # Define your actions.
    your_actions = dict(
        holding = 0,
        buy_1 = +1,
        sell_2 = -2,
    )

    # Create your agent.
    a1 = YourAgentClassName(
        your_id,
        your_actions,
        )

    # Create your market environment.
    env = gym.make("Market")

    # Select your id and mode to participate
    env.participate(your_id, mode)

    # reset fetches the initial state of the crypto market.
    obs = env.reset()

    # Perform real-time reinforcement learning
    for t in count():
        # Call act for the agent to take an action
        action = a1.act(obs)

        # To send your action to market:
        next_obs, rewards, done, _ = env.step(**action)

        # It is recommended that reward override and user-defined function usage be done via postprocess function.
        a1.postprocess(obs, action, next_obs, rewards)
```

## Setup details

### mode

- There are 2 modes: TEST and HACKATHON.
- Your agent will start trading in HACKATHON mode. This will affect the virtual KRW balance provided by Seoul AI.
- You can train your agent in the TEST mode. We advice you to train your agent before trying out the HACKATHON mode.

#### env.reset() in TEST mode

```python
your_id = "seoul_ai"
mode = Constants.TEST

env = gym.make("Market")
env.participate(your_id, mode)

# IF you call reset in TEST mode, your cash and balance will be updated to 100,000,000 KRW and 0.0 respectively.
obs = env.reset()
...
```

#### env.reset() in HACKATHON mode

```python
your_id = "seoul_ai"
mode = Constants.HACKATHON

env = gym.make("Market")
env.participate(your_id, mode)

# Calling reset in HACKATHON mode fetches the cash and balance
# It is different from calling reset in TEST mode as your cash and balance will not be reset.
obs = env.reset()
...
```

### act

```python
action = a1.act(obs)
```
The act function calls the following functions.
- preprocess() = changes raw data fetched by obs to state
- algo() = performs trading as defined by the participant.

    
### step
The step function fetches and saves the crypto market state so that the agent may start trading. This function returns 3 variables.

#### `obs`
obs is short for observation.
The datasets in obs are as follows:

```python
order_book = obs.get("order_book")    # {timestamp, ask price, ask_size, bid price, bid size}
trade = obs.get("trade")    # {timestamp, price, volume, ask_bid, sid} (the last 200 time series data)
agent_info = obs.get("agent_info")    # {cash, balance amount}
portfolio_rets = obs.get("portfolio_rets")    # {portfolio indicators based on algorithm performance}
```

#### `rewards`

There are 8 types of rewards

```python
rewards = dict(
    return_amt=return_amt,    # Return(amount) from current action
    return_per=return_per,    # Return(%) from current action
    return_sign=return_sign,    # 1 if profited from current action. -1 if loss. else 0
    fee=fee,    # Fee from current action
    hit=hit,    # 1 if buy and price goes up or sell and price goes down. else 0.
    real_hit=real_hit,    # Fee based hit
    score_amt=score_amt,    # Return(amount) from initial cash (100,000,000 KRW)
    score=score)    # Return(%) from initial cash (100,000,000 KRW) = hackathon score

```

#### `done`
The value of done is always False.


### Developing Agent class

#### Creating your agent

```python
import seoulai_gym as gym
from seoulai_gym.envs.market.agents import Agent

# Your agent must inherit from Seoul AI's agent class
class YourAgentClassName(Agent):

    # You need to develop 4 functions.
    __init__()
    preprocess()
    algo()
    postprocess()
```

#### init(set actions)

All participants must define the actions dictionary.

```python
def __init__(
    self,
    agent_id: str,
):

    """ Actions Dictionary
        key = action name, value = order parameters
        Use any action name
        Buy order'll be concluded at the first sell price
        Sell order'll be concluded at the first buy price.
        The probability of conclusion'll be 100%.
    """

    your_actions = dict(
        # You have to define holding action!
        holding = 0,

        # + means buying, - means selling.
        buy_1 = +1,    # buy_1 means that you will buy 1 bitcoin.
        sell_2 = -2,  # sell_2 means that you will sell 2 bitcoin.

        # 4th decimal place
        buy_1_2345 = +1.2345,
        sell_2_001 = -2.001,

        # You can define actions by %. However, integer between -100 and 100 must be entered.
        buy_all = (+100, '%'),    # buy_all means that you will buy 100% of the purchase amount
        sell_20per = (-20, '%'),    # sell_20per means you will sell 20% of the available volume
    )
    super().__init__(agent_id, your_actions)
    ...
```

#### preprocess

You can select your data from raw data (fetched by obs), and change it as you'd like. We encourage that you perform data normalization.

- preprocess is optional. If omitted, obs is entered as state.

```python
    def preprocess(
        self,
        obs,
    ):
        # get data
        trades = obs.get("trade")

        # make your own data!
        price_list = trades.get("price")
        cur_price = price_list[0]
        price10 = price_list[:10]

        ma10 = np.mean(price10)
        std10 = np.std(price10)
        thresh_hold = 1.0

        # obs -> state
        your_state = dict(
            buy_signal=(cur_price > ma10 + std10*thresh_hold),
            sell_signal=(cur_price < ma10 - std10*thresh_hold),
        )

        return your_state
```

#### algo (algorithm definition)

It is a function that defines the conditions for trading.
algo function must return self.action function.

```python
    def algo(
        self,
        state,
    ):
        if state["buy_signal"]:
            # Enter action_name as a parameter of actions dictionary.
            return self.action("buy_all")
        elif state["sell_signal"]:
            return self.action("sell_20per")
        else:
            return self.action(0)    # You can enter the index of the action_name as a parameter.
```

#### postprocess

You can select and redifine reward through the postprocess.

```python
    def postprocess(
        self,
        obs,
        action,
        next_obs,
        rewards,
    ):
        your_reward = 0

        # Select
        your_rewards = rewards.get("hit")

        # Redefine
        trades = obs.get("trade")
        next_trades = next_obs.get("trade")

        cur_price = trades["price"][0]
        next_price = next_trades["price"][0]

        change_price = (next_price-cur_price)

        your_reward = np.sign(change_price)
```

#### DQN Example

<a href="https://github.com/seoulai/gym/blob/market/examples/market/dqn_example.py">dqn_example.py</a>

#### Rule based Example

<a href="https://github.com/seoulai/gym/blob/market/examples/market/mean_reverting_example.py">mean_reverting_example.py</a>

#### Random Example

<a href="https://github.com/seoulai/gym/blob/market/examples/market/random_agent_example.py">random_agent_example.py</a>
