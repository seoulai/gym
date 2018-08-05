"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""
import random
from typing import Dict

from seoulai_gym.envs.mighty.agents import Agent
from seoulai_gym.envs.mighty.base import Constants
from seoulai_gym.envs.mighty.rules import Rules


class RandomAgent(Agent):
    def __init__(
        self,
        name: str,
        uid: int,
    ):
        """Initialize random agent.

        Args:
            name: (str) name of agent
            uid: (int)
        """
        super().__init__(name, uid)

        print("Initialize random agent : %ith player %s " % (uid, name))

    def act(
        self,
        obs: Dict,
        reward: int,
        done: bool,
    ) -> Dict:
        """
        Act randomly.

        Args:
            obs: (Dict) information about the current game status
            reward: (int) reward for perfomed step
            done: (float) information about end of game

        Return:
            act: (Dict)
        """
        board = obs["board"]
        game = obs["game"]

        print("[agent-act] %s %dth player (%s)" % (game.status, self._uid, self._name))
        if game.status == Constants.status_bidding:
            hand_cards = board.PLAYER_CARDS[self._uid]
            max_contract = game.contract

            # 최고 공약보다 높은 공약 있으면 제시
            contract = random.choice(range(0, 17))
            suit = random.choice(["s", "d", "c", "h"])

            if contract > 13 and contract > max_contract:
                act = {}
                act["contract"] = contract
                act["suit"] = suit
                print("\t%d %s" % (contract, suit))
                return act
            else:
                print("\tNone")
                return None
        elif game.status == Constants.status_choose_card:
            hand_cards = board.PLAYER_CARDS[self._uid]
            act = {}
            act["card"] = random.choice(hand_cards)
            return act

        elif game.status == Constants.status_contract:
            hand_cards = board.PLAYER_CARDS[self._uid]
            max_contract = game.contract

            # 최고 공약보다 높은 공약 있으면 제시
            contract = random.choice(range(0, 20))
            suit = random.choice(["s", "d", "c", "h"])

            if contract > max_contract:
                act = {}
                act["contract"] = contract
                act["suit"] = suit
                print("\t%d %s" % (contract, suit))
                return act
            else:
                print("\tNone")
                return None
        elif game.status == Constants.status_friend:
            friend = random.choice(["s-1", "d-1", "c-1", "h-1"])
            print("\t%s" % friend)
            act = {}
            act["friend"] = friend
            return act

        elif game.status == Constants.status_play:
            # 카드 제출
            valid_cards = Rules.get_valid_cards(self._uid, board, game)

            act = {}
            act["card"] = random.choice(valid_cards)

            # TODO validate card

            return act

        else:
            raise NotImplementedError(game.status)
