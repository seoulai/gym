"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""
from seoulai_gym.envs.mighty.agents import Agent
from typing import List
from typing import Tuple
from typing import Dict

from seoulai_gym.envs.mighty.base import Constants
from seoulai_gym.envs.mighty.rules import Rules

import random

class RandomAgent(Agent):
    def __init__(
        self,
        name: str,
        uid: int,
        #ptype: int,
    ):
        """Initialize random agent.

        Args:
            name: name of agent.
            ptype: type of piece that agent is responsible for.
        """
        super().__init__(name,uid)

        print('Initialize random agent : %ith player %s ' % (uid, name))

    def act(
        self,
        obs: Dict,
        reward: int,
        done: bool,
    ) -> int:
    #) -> Tuple[int, int, int, int]:
        """
        Choose a piece and its possible moves randomly.
        Pieces and moves are chosen from all current valid possibilities.

        Args:
            board: information about positions of pieces.
            reward: reward for perfomed step.
            done: information about end of game.

        Returns:
            Current and new location of piece.
        """
        #board_size = len(board)
        #valid_moves = self.generate_valid_cards(board, self, board_size)


        board = obs['board']
        game = obs['game']


        print('[agent-act] %s %dth player (%s)' % (game.status, self._uid, self._name))
        if game.status == Constants.status_bidding:
            hand_cards = board.PLAYER_CARDS[self._uid]
            max_contract = game.contract

            #최고 공약보다 높은 공약 있으면 제시
            contract = random.choice(range(0,17))
            suit = random.choice(['s','d','c','h'])

            if contract > 13 and contract > max_contract:
                act = {}
                act['contract'] = contract
                act['suit'] = suit
                print ('\t%d %s' % (contract, suit))
                return act
            else:
                print('\tNone')
                return None
        elif game.status == Constants.status_choose_card:
            hand_cards = board.PLAYER_CARDS[self._uid]
            act = {}
            act['card'] = random.choice(hand_cards)
            return act

        elif game.status == Constants.status_contract:
            hand_cards = board.PLAYER_CARDS[self._uid]
            max_contract = game.contract

            # 최고 공약보다 높은 공약 있으면 제시
            contract = random.choice(range(0, 20))
            suit = random.choice(['s', 'd', 'c', 'h'])

            if contract > max_contract:
                act = {}
                act['contract'] = contract
                act['suit'] = suit
                print('\t%d %s' % (contract, suit))
                return act
            else:
                print('\tNone')
                return None
        elif game.status == Constants.status_friend:
            friend = random.choice(['s-1', 'd-1', 'c-1', 'h-1'])
            print('\t%s' % friend)
            act = {}
            act['friend'] = friend
            return act

        elif game.status == Constants.status_play:
            # 카드 제출
            #hand_cards = board.PLAYER_CARDS[self._uid]
            valid_cards = Rules.get_valid_cards(self._uid,board,game)

            act = {}
            act['card'] = random.choice(valid_cards)

            # TODO validate card

            return act

        else:
            raise ("not implemented status " + game.status)

