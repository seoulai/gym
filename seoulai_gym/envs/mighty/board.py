"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""
from random import shuffle
from typing import Tuple
from typing import Dict

from seoulai_gym.envs.mighty.base import Constants


class Board(object):
    def __init__(
        self,
    ):
        """Board constructor.
        """
        self.PLAYER_CARDS = {}
        self.init()

    # 모든 변수 초기화(누적점수 제외)
    def init(
        self,
    ) -> None:
        # 전체카드 섞기
        self.ALL_CARDS = ["s-1", "s-k", "s-q", "s-j", "s-0", "s-9",
                          "s-8", "s-7", "s-6", "s-5", "s-4", "s-3", "s-2"]
        self.ALL_CARDS.extend(["d-1", "d-k", "d-q", "d-j", "d-0", "d-9",
                               "d-8", "d-7", "d-6", "d-5", "d-4", "d-3", "d-2"])
        self.ALL_CARDS.extend(["c-1", "c-k", "c-q", "c-j", "c-0", "c-9",
                               "c-8", "c-7", "c-6", "c-5", "c-4", "c-3", "c-2"])
        self.ALL_CARDS.extend(["h-1", "h-k", "h-q", "h-j", "h-0", "h-9", "h-8",
                               "h-7", "h-6", "h-5", "h-4", "h-3", "h-2", "jok"])

        shuffle(self.ALL_CARDS)

        # player 카드 클리어
        self.PLAYER_CARDS = {}

        # Agent에게 카드 분배(10장씩)
        for i in range(0, 5):
            # 소팅
            self.PLAYER_CARDS[i] = self.sort_handcard(self.ALL_CARDS[i*10:(i+1)*10])

        # 나머지 카드
        self.BONUS_CARDS = self.ALL_CARDS[-3:]

        # 선택된 카드
        self.SELECTED_CARD = {}

        # 게임
        self.FACE_CARDS = {}
        self.POINT_CARDS = {}

    # 무늬별 카드 정렬
    def sort_handcard(self, handcard):
        tmp_handcard = []
        tmp2_handcard = []
        power_suit = [Constants.suit_spade,
                      Constants.suit_diamond,
                      Constants.suit_clover,
                      Constants.suit_heart,
                      Constants.suit_joker]
        power_num = ["2", "3", "4", "5", "6", "7", "8", "9", "0", "j", "q", "k", "1"]

        for card in handcard:
            tmp_power = power_suit.index(card[0])*100
            tmp_power += power_num.index((card[2]))
            tmp_handcard.append((card, tmp_power))

        tmp_handcard = sorted(tmp_handcard, key=lambda card: card[1])

        for card in tmp_handcard:
            tmp2_handcard.append(card[0])
        return tmp2_handcard

    def move(
        self,
        agent,
        card,
    ) -> Tuple[Dict, int, bool, Dict]:
        obs = None
        reward = 0
        done = False
        info = None
        return obs, reward, done, info
