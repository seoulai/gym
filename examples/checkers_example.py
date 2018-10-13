"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""
import seoulai_gym as gym
from seoulai_gym.envs.checkers.agents import RandomAgentLight
from seoulai_gym.envs.checkers.agents import RandomAgentDark


def main():
    env = gym.make("Checkers")

    a1 = RandomAgentLight()
    a2 = RandomAgentDark()

    obs = env.reset()

    current_agent = a1
    next_agent = a2

    while True:
        from_row, from_col, to_row, to_col = current_agent.act(obs)
        obs, rew, done, info = env.step(current_agent, from_row, from_col, to_row, to_col)
        current_agent.consume(obs, rew, done)

        if done:
            print(f"Game over! {current_agent} agent wins.")
            obs = env.reset()

        # switch agents
        temporary_agent = current_agent
        current_agent = next_agent
        next_agent = temporary_agent

    env.close()


if __name__ == "__main__":
    main()
