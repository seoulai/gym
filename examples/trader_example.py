"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import seoulai_gym as gym
from seoulai_gym.envs.traders.agents import RandomAgentBuffett


def main():
  env = gym.make("Market")
  balance = 10000000
  a1 = RandomAgentBuffett("Buffett", balance)

  obs = env.reset()
  current_agent = a1

  rew = 0  # reward
  done = False

  while True:
    decision, price, volumn = current_agent.act(obs, rew, done)
    try:
      obs, rew, done, info = env.step(
          current_agent, decision, price, volumn)
    except ValueError:
      # print(f"Invalid action by {current_agent} agent.")
      break

    # render later
    # env.render()

    if done:
      print("done. Agent balance: ", current_agent._wallet)

      obs = env.reset()

  env.close()


if __name__ == "__main__":
  main()
