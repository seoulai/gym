"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""
from copy import deepcopy
from typing import Dict
from typing import List

from seoulai_gym.envs.mighty.base import Constants
from seoulai_gym.envs.mighty.board import Board


class Rules(object):
    @staticmethod
    def get_valid_cards(
        uid: int,
        board: Board,
        game: Constants.GAME,
    ) -> List[str]:
        hand_cards = deepcopy(board.PLAYER_CARDS[uid])
        valid_cards = deepcopy(board.PLAYER_CARDS[uid])

        # - 조커 사용, 효력, 조커콜
        if uid != game.start_player and game.jokercall:
            for card in valid_cards:
                if card == Constants.card_joker:
                    return [Constants.card_joker]

        # 해당 턴의 첫번째 플레이어가 낸 무늬만 낼 수 있음
        if game.start_player == uid:
            # - 주공 첫판 기루다x
            if game.president_player._uid == uid and game.round == 1:
                for card in hand_cards:
                    if card[0] == game.giruda:
                        valid_cards.remove(card)
        else:
            # start_player가 낸 무늬가 있으면 그것만 낼 수 있음
            has_suit = False
            for card in valid_cards:
                if card[0] == game.round_suit:
                    has_suit = True
                    break

            if has_suit:
                for card in hand_cards:
                    if card[0] != game.round_suit:
                        # 마이티, 조커는 예외
                        if card == game.mighty_card or card == Constants.card_joker:
                            pass
                        else:
                            valid_cards.remove(card)
            else:
                # 없으면 다른 카드 낼 수 있음
                pass
        if len(valid_cards) == 0:
            Rules.get_valid_cards(uid, board, game)
        return valid_cards

    @staticmethod
    def is_valid_card(
        board_list: Dict,
        card: str,
    ) -> bool:
        ret = False
        if card in Rules.get_valid_cards(board_list):
            ret = True
        return ret

    @staticmethod
    def get_round_winner(
        game: Constants.GAME,
        board: Board,
    ) -> int:
        winner = -1
        max_power = -1

        for player in board.FACE_CARDS:
            power = Rules.get_power(board.FACE_CARDS[player], game, board)
            if power > max_power:
                max_power = power
                winner = player
        return winner

    @staticmethod
    # 카드 별 파워. 마이티 > 조커(일반) > 기루다 > 라운드 카드 > 조커(1라운드, 10라운드, 조커콜)
    def get_power(card, game, board):
        power = 0
        if card == game.mighty_card:
            power = 1000
        elif card == Constants.card_joker:
            if game.round == 1 or game.round == 10:
                power = 0
            elif game.jokercall:
                power = 0
            else:
                power = 999
        elif card[0] == game.giruda:  # game suit
            card_num = card[2]
            if card_num == "1":
                power = 14
            elif card_num == "2":
                power = 2
            elif card_num == "3":
                power = 3
            elif card_num == "4":
                power = 4
            elif card_num == "5":
                power = 5
            elif card_num == "6":
                power = 6
            elif card_num == "7":
                power = 7
            elif card_num == "8":
                power = 8
            elif card_num == "9":
                power = 9
            elif card_num == "0":
                power = 10
            elif card_num == "j":
                power = 11
            elif card_num == "q":
                power = 12
            elif card_num == "k":
                power = 13
            power += 100
        elif card[0] == game.round_suit:  # trick_suit
            card_num = card[2]
            if card_num == "1":
                power = 14
            elif card_num == "2":
                power = 2
            elif card_num == "3":
                power = 3
            elif card_num == "4":
                power = 4
            elif card_num == "5":
                power = 5
            elif card_num == "6":
                power = 6
            elif card_num == "7":
                power = 7
            elif card_num == "8":
                power = 8
            elif card_num == "9":
                power = 9
            elif card_num == "0":
                power = 10
            elif card_num == "j":
                power = 11
            elif card_num == "q":
                power = 12
            elif card_num == "k":
                power = 13
        else:
            pass
        return power

    @staticmethod
    # 점수카드 갯수 계산
    def get_point(
        face_cards: Dict,
    ) -> int:
        # TODO get_point
        point_cards = ["s-1", "s-k", "s-q", "s-j", "s-0",
                       "d-1", "d-k", "d-q", "d-j", "d-0",
                       "c-1", "c-k", "c-q", "c-j", "c-0",
                       "h-1", "h-k", "h-q", "h-j", "h-0"]
        point_card = []
        for uid in face_cards:
            face_card = face_cards[uid]
            if face_card in point_cards:
                point_card.append(face_card)
        return point_card
