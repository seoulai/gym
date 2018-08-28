# Seoul AI Gym

**Seoul AI Gym is a toolkit for developing AI algorithms.**
This `gym` simulates environments and enables you to apply any teaching technique on agent.

[![Build Status](https://api.travis-ci.com/seoulai/gym.svg?branch=master)](https://travis-ci.com/seoulai/gym)

Seoul AI Gym was inspired by [OpenAI gym](https://github.com/openai/gym) and tries to follow its API very closely.


### Contents
* [Basics](https://github.com/seoulai/gym#basics)
* [Installation](https://github.com/seoulai/gym#installation)
  * [`pip3`](https://github.com/seoulai/gym#pip3)
  * [From source](https://github.com/seoulai/gym#from-source)
* [Environments](https://github.com/seoulai/gym#environments)
* [Examples](https://github.com/seoulai/gym#examples)
* [Testing](https://github.com/seoulai/gym#testing)

## Basics
There are two terms that are important to understand: *Environment* and *Agent*.

An environment is a world (simulation) with which an agent can interact.
An agent can observe a world and act based on its decision.

`seoulai-gym` provides environments.
An example of creating environment:

```python
import seoulai_gym as gym
env = gym.make("Checkers")
```

Every environment has three important methods: `reset`, `step` and `render`.

##### `reset(self) -> observation`
Reset an environment to default state and return `observation` of default state.
`observation` data structure depends on environment and is described separately for each environment.

##### `step(self, agent, action) -> observation, reward, done, info`
Perform an `action` on behalf of `agent` in environment lastly observed by either `reset` or `step`.
An `action` can differ among different environments but the return value of `step` method is always same.
A `reward` is given to an agent when action that was done in the current step or some of the previous steps have led to a positive outcome for an agent (e.g winning a game).
An `info` is a dictionary containing extra information about performed `action`.

##### `render(self) -> None`
Display state of game on a screen.


## Installation
There are two ways to install `seoulai-gym`.

#### `pip3`
The recommended way for developers creating an agent is to install `seoulai-gym` using `pip3`.
```
pip3 install seoulai-gym
```

#### From source
You can also clone and install `seoulai-gym` from source.
This option is for developers that want to create new environments or modify existing ones.

```shell
git clone https://github.com/seoulai/gym.git
cd gym
pip3 install -e .
```

#### Supported systems
`seoulai-gym` requires to have at least Python 3.6 and was tested on Arch Linux, macOS High Sierra and Windows 10.

## Environments
Currently, environment simulating game of [Checkers](https://en.wikipedia.org/wiki/Draughts), [Mighty] (https://en.wikipedia.org/wiki/Mighty_(card_game)), and Market are provided.

* Checkers
  ```python
  import seoulai_gym as gym
  env = gym.make("Checkers")
  env.reset()
  env.render()
  ```

* Mighty
  ```python
  import seoulai_gym as gym
  from seoulai_gym.envs.mighty.agent.RandomAgent import RandomAgent

  env = gym.make("Mighty")
  players = [RandomAgent("Agent 1", 0),
              RandomAgent("Agent 2", 1),
              RandomAgent("Agent 3", 2),
              RandomAgent("Agent 4", 3),
              RandomAgent("Agent 5", 4)]
  obs = env.reset()
  obs["game"].players = [
    players[0]._name,
    players[1]._name,
    players[2]._name,
    players[3]._name,
    players[4]._name,
    ]
  env.render()

* Market

  ```python
  import seoulai_gym as gym
  from seoulai_gym.envs.traders.agents import RandomAgentBuffett

  # make enviroment
  env = gym.make("Market")

  # select exchange
  env.select("upbit")

  init_cash = 100000000  # KRW
  a1 = RandomAgentBuffett("Buffett", init_cash)
  current_agent = a1

  env.reset()
  env.render()
  ```

## Examples

* Checkers
  * https://github.com/seoulai/gym/blob/master/examples/checkers_example.py

    [![Watch the video](https://i.ytimg.com/vi/O-Q9hg7Vng8/hqdefault.jpg)](https://youtu.be/O-Q9hg7Vng8)

* Mighty
  * https://github.com/seoulai/gym/blob/master/examples/mighty_example.py

    [![Watch the video](http://img.youtube.com/vi/M3GCt8evGkQ/0.jpg)](https://youtu.be/M3GCt8evGkQ?t=0s)

* Market
  * https://github.com/seoulai/gym/blob/master/examples/trader_example.py


## Testing
All test are written using [pytest](http://doc.pytest.org/).
You can run them via:

```
pytest
```
