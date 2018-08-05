"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""
import random
from typing import Dict
from typing import List
from typing import Tuple

from seoulai_gym.envs.mighty.agents import Agent
from seoulai_gym.envs.mighty.base import Constants
from seoulai_gym.envs.mighty.rules import Rules


class AlangAgent(Agent):
    def __init__(
        self,
        name: str,
        uid: int,
    ):
        """Initialize Alang agent.

        Args:
            name: (str) name of agent
            uid: (int)
        """
        super().__init__(name, uid)

        self.contract = 0
        self.suit = ""
        self.friend = ""

        print("Initialize alang agent : %ith player %s " % (uid, name))

    # 공약 설정
    def makeContract(
        self,
        hand_card: List,
    ) -> Tuple[int, str, str]:  # 공약, 기루다, 프렌드
        """
        contract = random.choice(range(0, 20))
        suit = random.choice(["s", "d", "c", "h"])
        friend = random.choice(["s-1","jok","first_turn"])
        """
        card_order = ["2", "3", "4", "5", "6", "7", "8", "9", "0", "j", "q", "k", "1"]
        suits = ["s", "h", "d", "c"]

        print("\tcard=", end=" ")
        print(",".join(hand_card))
        # 1 기루다 모양 결정
        max_power = 0
        for s in suits:
            power = 0
            mighty = "s-1"
            if s == "s":
                mighty = "d-1"

            # 1.1 카드 무늬별로 power 계산(1.마이티 존재/기루다 갯수, 2. 센카드 숫자
            max_num = 0
            for card in hand_card:
                # 마이티 존재(100)
                if mighty == card:
                    power += 100
                # 기루다 갯수(100*n)
                if s in card:
                    power += 100
                    # 가장 센카드(2~1)
                    cur_num = card_order.index(card[2])
                    if cur_num > max_num:
                        max_num = cur_num
            power += max_num
            print("\tsuit=%s, power=%i" % (s, power))
            # 1.2 power 가장 큰 카드로 기루다 모양 결정
            if power > max_power:
                max_power = power
                self.suit = s

        print("\tfinal suit = " + self.suit)

        # 2 기루다 아닌 보스카드 갯수
        num_bosscard = 0
        card_order.reverse()
        for s in suits:
            # 2.1 갯수 = 기루다 제외한 카드 무늬별로, 카드 ace부터 연결된 카드 + 조커
            if s == self.suit:
                continue

            for i in card_order:  # 카드ace부터
                card = "%s-%s" % (s, i)
                if card in hand_card:
                    num_bosscard += 1
                else:
                    break
        if "jok" in hand_card:
            num_bosscard += 1
        print("\tbosscard : " + str(num_bosscard))

        # 3 프렌드 결정(마이티->조커->첫턴)
        mighty = "s-1"
        if self.suit == "s":
            mighty = "d-1"

        if mighty not in hand_card:
            self.friend = "mighty"
        elif "jok" not in hand_card:
            self.friend = "jok"
        else:
            self.friend = "first"
        print("\tfriend : " + self.friend)

        # 4 위닝턴 계산
        # 4.1 위닝턴 = 기루다 갯수 + 기루다 아닌 보스카드 갯수 + 프렌드help(1) + 추가카드(1)
        winning_turn = int(max_power / 100) + num_bosscard + 1 + 1
        print("\twinning_turn : " + str(winning_turn))

        # 5 공약 결정
        # 4.1 contract (win 10-> cont 16, 9->15, 8->14, 7이하->pass
        if winning_turn >= 10:
            self.contract = 16
        elif winning_turn == 9:
            self.contract = 15
        elif winning_turn == 8:
            self.contract = 14
        else:
            self.contract = 0
        print("\tcontract : " + str(self.contract))

        # 공약, 기루다, 프렌드 반환
        return (self.contract, self.suit, self.friend)

    def removeCard(
        self,
        hand_cards: List,
    ) -> str:
        # 기루다, 마이티, 조커, 보스카드  빼고 랜덤으로 버림
        candidate_cards = []

        mighty = "s-1"
        if self.suit == "s":
            mighty = "d-1"

        for card in hand_cards:
            if card == mighty:  # 마이티
                continue
            elif card == "jok":
                continue
            elif card[0] == self.suit:  # 기루다
                continue
            elif card[2] == "1":
                continue
            else:
                candidate_cards.append(card)

        return random.choice(candidate_cards)

    def get_low_card(
        self,
        valid_cards: List,
    ) -> str:
        low_card = ""
        # 기루다 다음으로 많은 무늬
        num_suit = {}
        for card in valid_cards:
            s = card[0]
            if s == self.suit:
                continue
            n = 0
            if s in num_suit:
                n = num_suit[s]
            num_suit[s] = n + 1

        max_num = 0
        max_suit = ""
        for s in num_suit:
            if num_suit[s] > max_num:
                max_num = num_suit[s]
                max_suit = s

        # 가장 낮은 카드
        card_order = ["2", "3", "4", "5", "6", "7", "8", "9", "0", "j", "q", "k", "1"]
        low_num = 13

        for card in valid_cards:
            if card[0] == max_suit:
                i = card_order.index(card[2])
                if i < low_num:
                    low_num = i
                    low_card = card

        if len(low_card) == 0:
            # 예외 상황. random 선택
            low_card = random.choice(valid_cards)
        return low_card

    def act(
        self,
        obs: Dict,
        reward: int,
        done: bool,
    ) -> int:
        """
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
            (contract, suit, friend) = self.makeContract(hand_cards)

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
            # 기루다, 마이티, 조커, 보스카드 빼고 랜덤으로 버림
            act["card"] = self.removeCard(hand_cards)
            print("removeCard")
            print("\thand_cards : " + ",".join(hand_cards))
            print("\tremove card: " + act["card"])
            return act

        elif game.status == Constants.status_contract:
            hand_cards = board.PLAYER_CARDS[self._uid]
            max_contract = game.contract

            # 최고 공약보다 높은 공약 있으면 제시
            (contract, suit, friend) = self.makeContract(hand_cards)

            if contract > 13 and contract > max_contract:
                act = {}
                act["contract"] = contract
                act["suit"] = suit
                print("\tcontract : %d %s" % (contract, suit))
                return act
            else:
                print("\tcontract : None")
                return None

        elif game.status == Constants.status_friend:
            print("\tfriend : %s" % self.friend)
            act = {}
            act["friend"] = self.friend
            return act

        elif game.status == Constants.status_play:
            # 카드 제출
            valid_cards = Rules.get_valid_cards(self._uid, board, game)

            selected_card = random.choice(valid_cards)

            # 보스카드
            boss_card = []
            for card in valid_cards:
                if card[0] == self.suit:
                    continue
                elif card[2] == "1":
                    boss_card.append(card)

            # 기루다 다음으로 많은 무늬 중 가장 낮은 카드
            low_card = self.get_low_card(valid_cards)

            # 1. 첫턴
            if game.round == 1:

                # 1.1. ‘노 기루다’가 아니면,
                if self.suit != "n":
                    # 1.1.1. 친구가 마이티
                    if self.friend == "mighty":
                        # 1.1.1.1. 첫 턴 보스카드가 있으면, 보스카드
                        if len(boss_card) != 0:
                            selected_card = random.choice(boss_card)
                        # 1.1.1.2. 보스카드가 없으면, 기루다 다음으로 많은 무늬 중 가장 낮은 카드
                        else:
                            selected_card = low_card
                    # 1.1.2. 친구가 조카이면,
                    elif self.friend == "jok":
                        # 1.1.2.1. 보스카드 있으면 보스카드
                        if len(boss_card) != 0:
                            selected_card = random.choice(boss_card)
                        # 1.1.2.2. 보스카드 없으면 (되도록 조카 친구를 안 불러야 했겠지만) 기루다 다음으로 많은 무늬 중 가장 낮은 카드
                        else:
                            selected_card = low_card
                    # 1.1.3. 친구가 첫 턴이라면,
                    else:  # 첫턴
                        # 1.1.3.1. 기루다 다음으로 많은 무늬 중 가장 낮은 카드
                        card = low_card
                else:  # 노기루다
                    # todo 노기루다 로직
                    raise("not implemented")

            # 2. 2턴
            elif game.round == 2:
                # 2.1. 1턴을 주공이 먹었다면, (=첫턴 친구는 아닌 경우)
                if game.start_player == self._uid and self._uid == game.president_player._uid:
                    # 2.1.1. 기루다 보스카드가 있다면, 보스카드
                    card = "%s-1" % (self.suit)
                    if card in valid_cards:
                        selected_card = card
                    # 2.1.2. 기루다 보스카드가 없다면,
                    else:
                        # 2.1.2.2.1. 조커가 없다면, (친구가 해결해주길 기대하면서) 기루다 중 제일 낮은 카드
                        # 2.1.2.2.2. 조커가 있다면,
                        # 2.1.2.2.1. 기루다 무늬 부르면서 조커 (친구가 헷갈리지 않도록 기루다 정리)
                        # 2.1.2.2.2. 기루다 중 제일 낮은 카드
                        pass

                # 2.2. 1턴을 친구가 먹고 기루다를 돌려줬다면, (=첫턴 친구이거나 마이티 친구인 경우)
                # 2.2.1. 마이티가 있다면, 마이티
                # 2.2.2. 마이티가 없다면,
                # 2.2.2.1. 기루다 보스카드가 있다면, 보스카드
                # 2.2.2.2. 기루다 보스카드가 없다면, 기루다 중 제일 낮은 카드

                # 2.3. 1턴을 못 먹고, 야당이나 친구가 기루다 아닌 무늬를 돌렸다면,
                # 2.3.1. 무늬가 없다면, 기루다 중 제일 낮은 카드
                # 2.3.2. 무늬가 있다면,
                # 2.3.2.1. 무늬 보스카드가 있다면, 보스카드
                # 2.3.2.2. 무늬 보스카드가 없다면,
                # 2.3.2.2.1. 조커가 있으면, 조커
                # 2.3.2.2.2. 조커가 없으면, 무늬 중 제일 낮은 카드

            else:
                selected_card = random.choice(valid_cards)

            # TODO validate card

            act = {}
            act["card"] = selected_card
            return act

        else:
            raise ("not implemented status " + game.status)
