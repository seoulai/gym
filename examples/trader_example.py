"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import seoulai_gym as gym
from seoulai_gym.envs.traders.agents import RandomAgentBuffett


def main():
  # initial state
  init_cash = 100000000
  fee_rt = 0.05/100
  state = [init_cash, fee_rt]

  # make Market Enviroment
  env = gym.make("Market", state)

  a1 = RandomAgentBuffett("Buffett")
  current_agent = a1
  
  obs = env.reset(state)
  #print("reset obs")
  #print(obs)

  rew = 0  # reward
  done = False

  #trading_episodes = 10
  #for trading_episode in range(0, trading_episodes):
    #print("trading_episode : %d"%trading_episode)
  while True:
    decision, trad_price, trad_qty = current_agent.act(obs, rew, done)
    try:
      obs, rew, done, info = env.step(
          current_agent, decision, trad_price, trad_qty)
    except ValueError:
      # print(f"Invalid action by {current_agent} agent.")
      break

    # render later
    # env.render()

    if done:
      wallet = env.cash+env.asset_val
      diff = wallet-init_cash
      print("done. Agent wallet: %f, Agent return : %f, Agent wallet ratio : %f "%(wallet, diff, (diff/init_cash)*100))
      obs = env.reset(state)
      break

  env.close()


if __name__ == "__main__":
  main()
