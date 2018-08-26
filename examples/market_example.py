"""
Cinyoung Hur, cinyoung.hur@gmail.com
James Park, laplacian.k@gmail.com
seoulai.com
2018
"""
import seoulai_gym as gym
from seoulai_gym.envs.market.agents import RandomAgentBuffett
from seoulai_gym.envs.market.agents import MRV1Agent    # MeanReverting Agent Version 1.0

def main():

    # make Market enviroment
    env = gym.make("Market")

    # select exchange
    # TODO: add trading condition of real exchanges.
    # then users will be able to choose exchange.
    env.select("upbit")

    init_cash = 100000000  # KRW
    #a1 = RandomAgentBuffett("Buffett", init_cash)
    a1 = MRV1Agent("MeanReverting", init_cash)
    current_agent = a1

    obs = env.reset()

    rew = 0  # reward
    done = False

    print("tick\t\t decision\t\t trad_price(ccld_price)\t\t"
          + "trad_qty(ccld_qty)\t\t fee\t\t cash\t\t asset_qty\t\t"
          + "asset_val\t\t portfolio_val\t\t 1tick_return\t\t 1tick_ret_ratio\t\t ")
    i = 0
    while True:
        decision, trad_price, trad_qty = current_agent.act(obs, rew, done)
        try:
            obs, rew, done, info = env.step(
                current_agent, decision, trad_price, trad_qty)
            # data sheet
            print("%5d %4s %10lf %10lf %10lf %10lf %10lf %10lf %10lf %10lf"
                  % (i, decision, trad_price, trad_qty, info["fee"],
                     current_agent.cash, current_agent.asset_qty,
                     current_agent.asset_val, info["1tick_return"],
                     info["1tick_ret_ratio"]))

        except ValueError:
            break

        env.render(current_agent, info, decision)

        if done:
            wallet = current_agent.cash+current_agent.asset_val
            diff = wallet-init_cash
            print("game over!!! " + info["msg"])
            print("total result. Agent wallet: % f, Agent total_return: % f, Agent total_ret_ratio : %f" %
                  (wallet, diff, ((wallet/init_cash)-1)*100))
            obs = env.reset()
            # reset agent
            current_agent = RandomAgentBuffett("Buffett", 100000000)

        i = i+1

    env.close()


if __name__ == "__main__":
    main()
