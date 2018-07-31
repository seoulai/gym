"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""
import seoulai_gym as gym
from seoulai_gym.envs.mighty.agent.RandomAgent import RandomAgent


def main():
    # gym 환경명
    env = gym.make("Mighty")

    # 플레이어 이름, uid
    players = [RandomAgent("Agent 1", 0),
               RandomAgent("Agent 2", 1),
               RandomAgent("Agent 3", 2),
               RandomAgent("Agent 4", 3),
               RandomAgent("Agent 5", 4)]

    # 환경 초기화
    obs = env.reset()

    # 플레이어 등록
    obs['game'].players = [players[0]._name, players[1]._name, players[2]._name, players[3]._name, players[4]._name]
    turn = 0

    reward = 0
    done = False

    num_of_game = 10  # 구동할 게임 수
    while True:
        act = players[turn].act(obs, reward, done)
        print('\t %s' % (act), end=':')
        print(obs['board'].PLAYER_CARDS[turn])
        obs, rew, done, info = env.step(players[turn], act)

        # switch agents
        if 'turn' in info:
            turn = info['turn']
        else:
            turn = (turn+1) % 5

        env.render()

        if done:
            num_of_game -= 1
            if num_of_game == 0:
                break
            obs = env.reset()

    input('end play')
    env.close()


if __name__ == "__main__":
    main()
