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


class BossAgent(Agent):
    def __init__(
        self,
        name: str,
        uid: int,
    ):
        """Initialize Boss agent.

        Args:
            name: (str) name of agent
            uid: (int)
        """
        super().__init__(name, uid)

        print("Initialize boss agent : %ith player %s " % (uid, name))

    def act(
        self,
        obs: Dict,
        reward: int,
        done: bool,
    ) -> int:
        board = obs["board"]
        game = obs["game"]

        print("[agent-act] %s %dth player (%s)" % (game.status, self._uid, self._name))
        if game.status == Constants.status_vote:
            hand_cards = board.PLAYER_CARDS[self._uid]
            max_contract = game.contract

            quality = [0, 10, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 4, 6]
            quantity = [0, 0, 9, 13, 14, 16, 18, 20, 20, 20, 20]
            myQualtity = {"s": 0, "d": 0, "c": 0, "h": 0}  # 무늬별 퀄리티
            myQuantity = {"s": 0, "d": 0, "c": 0, "h": 0}  # 무늬별 갯수

            for card in hand_cards:
                suit = card[0]
                num = card[2]
                if num == "j":
                    num = 11
                elif num == "q":
                    num = 12
                elif num == "k":
                    num = 13

                # jok
                if card == "jok":
                    for i in range(0, 4):
                        myQuantity[i] = myQuantity[i] + 6
                        myQuantity[i] = myQuantity[i] + 1
                else:
                    myQualtity[suit] = myQualtity[suit] + quality[num]
                    myQuantity[i] = myQuantity[i] + 1

            for s in myQualtity.keys():
                if myQualtity[s] > 20:
                    myQualtity[s] = 20

            # 가장 높은 score를 가지는 suit 선택
            max_suit = "c"
            max_score = -1
            for s in myQualtity.keys():
                scoreQuality = myQualtity[s]
                scoreQuantity = quantity[myQuantity[s]]
                if scoreQuality + scoreQuantity == 0:
                    continue

                score = (2 * scoreQuality * scoreQuantity / (scoreQuality + scoreQuantity))  # 조화평균
                if score > max_score:
                    max_score = score
                    max_suit = s

            # 마이티 있으면 +2
            mighty = "s-1"
            if max_suit == "s":
                mighty = "d-1"
            if mighty in hand_cards:
                max_score += 2

            # 초구 없으면 -1 or -2
            cards = ["s-1", "d-1", "h-1", "c-1", "d-k", "s-k"]
            cards.remove(max_suit+"-1")  # 기루다-1
            cards.remove(mighty)
            if max_suit == "s":
                cards.remove("s-k")
            else:
                cards.remove("d-k")
            # TODO needFirstWin = True
            for card in cards:
                if card in hand_cards:
                    # TODO needFirstWin = False
                    break
            max_score -= 1
            if max_score > 16:  # 공약 높으면 초구 위력이 커진다
                max_score -= 1

            if max_score > 13 and max_score > max_contract:
                # 16이상이면 max에서 2뺀다
                if max_score >= 16:
                    max_score -= 2

                act = {}
                act["contract"] = max_score
                act["suit"] = max_suit
                print("\t%d %s" % (max_score, max_suit))
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
