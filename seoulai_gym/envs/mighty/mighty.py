"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018

Mighty
https://en.wikipedia.org/wiki/Mighty_(card_game)
https://ko.wikipedia.org/wiki/%EB%A7%88%EC%9D%B4%ED%8B%B0_(%EC%B9%B4%EB%93%9C_%EA%B2%8C%EC%9E%84)
"""
import copy
import random
import sys
from typing import Dict
from typing import Tuple

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QEventLoop, QTimer

from seoulai_gym.envs.mighty.base import Constants
from seoulai_gym.envs.mighty.rules import Rules
from seoulai_gym.envs.mighty.board import Board
from seoulai_gym.envs.mighty.graphics import Graphics


RENDER_TIME = 10  # 화면 출력 후 대기 시간
FRIEND_REVEAL_TIME = 1000  # 프렌드 드러난 뒤 대기 시간
JOKERCALL_REVEAL_TIME = FRIEND_REVEAL_TIME  # 조커콜
JOKER_REVEAL_TIME = FRIEND_REVEAL_TIME  # 첫턴 조커
GAME_END_TIME = 1000  # 게임 종료 후 대기 시간


class Mighty(Constants, Rules):
    def __init__(
        self,
        state: str=None,
    ) -> None:
        """Initialize checkers board and its visualization.

        Args:
            state: Optional, path to saved game state. TODO

        Return:
            None
        """
        self.app = QApplication(sys.argv)

        self.board = Board()
        self.graphics = Graphics()
        self.GAME = Constants.GAME()
        self.done = False

    def step(
        self,
        agent,
        act: Dict,
    ) -> Tuple[Dict, int, bool, Dict]:
        """Make a step (= move) within board.

        Args:
            agent: Agent making a move.
            act:

        Return:
            obs: Information about positions of pieces.
            rew: Reward for perfomed step.
            done: Information about end of game.
            info: Additional information about current step.
        """

        info = {}  # 지금은 turn만 설정
        point = 0

        if self.GAME.status == Constants.status_bidding:  # 공약 제시
            # self.GAME.notice = Constants.status_bidding
            self.GAME.notice = ""

            contract = None
            suit = None
            if len(self.GAME.bidder) == 0:  # 남은 입찰자가 없으면
                print("\nno contract.. reset game\n")
                self.GAME.notice = "reset"
                self.render(1000)
                self.GAME.notice_player = {}
                self.reset()
            elif len(self.GAME.bidder) == 1:  # 남은 입찰자가 1명이라면
                if self.GAME.bidder[0] == agent._uid:  # 남은 입찰자가 나라면
                    if self.GAME.contract == 0:  # 모두 pass한 경우, 새로 시작
                        self.GAME.notice_player[agent._uid] = "pass"
                        self.GAME.bidder.remove(agent._uid)
                        info["turn"] = agent._uid
                    else:
                        self.GAME.status = Constants.status_choose_card
                        self.GAME.president_player = agent
                        self.board.PLAYER_CARDS[agent._uid].extend(self.board.BONUS_CARDS)
                        self.board.BONUS_CARDS = []
                        print("president is " + agent._name)
                        print("\t%s %d" % (self.GAME.giruda, self.GAME.contract))
                        info["turn"] = agent._uid

                    # 플레이모드 체크(round)
                    if self.graphics.btnset.PLAYMODE == Constants.playmode_round:
                        self.graphics.btnset.PLAYMODE = Constants.playmode_pause

                else:
                    pass
            else:  # 입찰자가 여러명이라면
                if act is None and agent._uid in self.GAME.bidder:
                    # 다음 입찰자 설정
                    info["turn"] = self.GAME.bidder[(self.GAME.bidder.index(agent._uid)+1) % len(self.GAME.bidder)]

                    # 입찰 가능 명단에서 제외
                    self.GAME.bidder.remove(agent._uid)
                    self.GAME.notice_player[agent._uid] = "pass"
                else:
                    if agent._uid in self.GAME.bidder:
                        # 입찰한 사람만 계속 공약 입찰 가능
                        contract = act["contract"]
                        suit = act["suit"]

                        # TODO check contract

                        # 공약 업데이트
                        if contract > self.GAME.contract:
                            self.GAME.president_player = agent
                            self.GAME.contract = contract
                            self.GAME.giruda = suit
                            self.GAME.notice_player[agent._uid] = "%s %d" % (suit, contract)

                        # TODO popup contract
            # 플레이모드 체크(step)
            self.render()
            if self.graphics.btnset.PLAYMODE == Constants.playmode_step:
                self.graphics.btnset.PLAYMODE = Constants.playmode_pause

        elif self.GAME.status == Constants.status_choose_card:  # 남은카드 3장 받고, 버릴카드 3장 선택
            # noti
            self.GAME.notice = "extra cards"
            self.render()
            self.GAME.notice = ""

            self.GAME.notice_player = {}
            self.GAME.notice_player[agent._uid] = "president"

            card = act["card"]

            # 선택된 카드 표시
            self.board.SELECTED_CARD = {}
            self.board.SELECTED_CARD[agent._uid] = self.board.PLAYER_CARDS[agent._uid].index(card)
            self.render()
            self.board.SELECTED_CARD = {}

            # 선택된 주공 카드 쓰레기통으로
            self.board.PLAYER_CARDS[agent._uid].remove(card)
            self.board.BONUS_CARDS.append(card)

            # 삭제 카드 출력
            print("\tremove   : " + card)
            print("\thandcard : " + ", ".join(self.board.PLAYER_CARDS[agent._uid]))

            # 3장 버렸으면 최종 공약
            if len(self.board.PLAYER_CARDS[agent._uid]) == 10:
                self.GAME.status = Constants.status_contract
                # 소팅
                self.board.PLAYER_CARDS[agent._uid] = self.sort_handcard(self.board.PLAYER_CARDS[agent._uid])

                # 플레이모드 체크(round)
                if self.graphics.btnset.PLAYMODE == Constants.playmode_round:
                    self.graphics.btnset.PLAYMODE = Constants.playmode_pause

            # 다음 턴도 주공
            info["turn"] = agent._uid

            # 플레이모드 체크(step)
            if self.graphics.btnset.PLAYMODE == Constants.playmode_step:
                self.graphics.btnset.PLAYMODE = Constants.playmode_pause

        elif self.GAME.status == Constants.status_contract:  # 주공이 최종 공약
            # noti
            self.GAME.notice = Constants.status_contract
            self.render()

            if act is not None:  # 최종 공약 있는 경우
                contract = act["contract"]
                suit = act["suit"]

                # check contract. suit 변경하면 최소 2 증가
                if self.GAME.giruda != suit:
                    if self.GAME.contract+2 <= contract:
                        pass
                    else:
                        self.GAME.contract += 2
                        print("\tinvalid contract.. contract changed : %d -> %d" % (contract, self.GAME.contract))
                # update contract
                self.GAME.contract = contract
                self.GAME.giruda = suit

            # 마이티카드, 조커콜카드 설정
            if self.GAME.giruda == Constants.suit_spade:
                self.GAME.mighty_card = "d-1"
            if self.GAME.giruda == Constants.suit_clover:
                self.GAME.jokercall_card = "h-3"

            print("\tcontract : " + str(self.GAME.contract))
            print("\tsuit     : " + self.GAME.giruda)
            print("\tmighty   : " + self.GAME.mighty_card)
            print("\tjokercall: " + self.GAME.jokercall_card)
            self.GAME.status = Constants.status_friend

            # 다음 턴도 주공
            info["turn"] = agent._uid

            # 플레이모드 체크(step)
            if self.graphics.btnset.PLAYMODE == Constants.playmode_step:
                self.graphics.btnset.PLAYMODE = Constants.playmode_pause

        elif self.GAME.status == Constants.status_friend:  # 주공이 친구 지정
            friend = act["friend"]
            self.GAME.friend_card = friend
            self.GAME.friend_player = self.GAME.president_player

            # 라운드1 시작
            self.GAME.status = Constants.status_play
            self.GAME.start_player = self.GAME.president_player._uid
            self.GAME.current_player = self.GAME.president_player._uid

            # 다음 턴도 주공
            info["turn"] = agent._uid
            self.GAME.notice_player = {}

            self.GAME.notice = friend + " friend"
            self.render()
            self.GAME.notice = ""

            # 플레이모드 체크(step)
            if self.graphics.btnset.PLAYMODE == Constants.playmode_step:
                self.graphics.btnset.PLAYMODE = Constants.playmode_pause

        elif self.GAME.status == Constants.status_play:  # 라운드 차례별 카드 제출
            # round 출력
            if self.GAME.start_player == agent._uid:
                # self.GAME.notice_player[agent._uid] = "round " + str(self.GAME.round)
                self.render()
                self.GAME.notice_player = {}
            else:
                self.GAME.notice_player = {}

            # 플레이모드 체크(step)
            if self.graphics.btnset.PLAYMODE == Constants.playmode_step:
                self.graphics.btnset.PLAYMODE = Constants.playmode_pause

            if True:  # TODO remove
                if True:
                    card = act["card"]

                    # TODO validate card

                    if len(self.board.FACE_CARDS) == 0:  # 첫턴
                        # 라운드 무늬 설정
                        self.GAME.round_suit = card[0]

                        # 조커 체크 - 무늬 없으면 임의로 변경
                        is_joker = False
                        if card == Constants.card_joker:
                            self.GAME.round_suit = random.choice([Constants.suit_spade,
                                                                  Constants.suit_diamond,
                                                                  Constants.suit_clover,
                                                                  Constants.suit_heart])
                            is_joker = True
                        elif card[1:] == "ok":  # sok,dok,cok,hok 인 경우 -> jok로 변경
                            card = Constants.card_joker
                            is_joker = True

                        # 조커면 무늬 노티
                        if is_joker:
                            self.GAME.notice = "joker: "
                            if self.GAME.round_suit == Constants.suit_spade:
                                self.GAME.notice += "spade"
                            elif self.GAME.round_suit == Constants.suit_diamond:
                                self.GAME.notice += "diamond"
                            elif self.GAME.round_suit == Constants.suit_clover:
                                self.GAME.notice += "clover"
                            elif self.GAME.round_suit == Constants.suit_heart:
                                self.GAME.notice += "heart"
                            self.render(JOKER_REVEAL_TIME)
                            self.GAME.notice = ""

                    # 조커콜 체크, 노티
                    if self.GAME.start_player == agent._uid and card == self.GAME.jokercall_card:
                        self.GAME.jokercall = True
                        self.GAME.notice = "joker call"
                        self.render(JOKERCALL_REVEAL_TIME)
                        self.GAME.notice = ""

                    # 프렌드 체크, 노티
                    friend_card = self.GAME.friend_card
                    if friend_card == Constants.card_mighty:
                        friend_card = "s-1"
                        if self.GAME.giruda == Constants.suit_spade:
                            friend_card = "d-1"

                    # 카드 올리기
                    self.board.SELECTED_CARD = {}
                    self.board.SELECTED_CARD[agent._uid] = self.board.PLAYER_CARDS[agent._uid].index(card)

                    if card == friend_card:
                        self.GAME.friend_player = agent
                        print("\treveal friend : " + agent._name)
                        self.GAME.notice_player[agent._uid] = "friend"
                        self.render(FRIEND_REVEAL_TIME)
                        self.GAME.notice_player = {}
                    else:
                        self.render()
                    self.board.SELECTED_CARD = {}

                    # 카드 제출
                    self.board.move(agent, card)
                    hand_cards = self.board.PLAYER_CARDS[self.GAME.current_player]
                    hand_cards.remove(card)
                    self.board.PLAYER_CARDS[self.GAME.current_player] = hand_cards
                    self.board.FACE_CARDS[self.GAME.current_player] = card
                    self.GAME.current_player = (self.GAME.current_player + 1) % 5

                # 모든 플레이어가 카드냈으면 정산
                if len(self.board.FACE_CARDS) == 5:
                    self.graphics.checkPLAYMODE()
                    # 플레이모드 체크(step)
                    if self.graphics.btnset.PLAYMODE == Constants.playmode_step:  # step -> pause
                        self.graphics.btnset.PLAYMODE = Constants.playmode_pause

                    # 승자 결정
                    self.GAME.current_player = Rules.get_round_winner(self.GAME, self.board)
                    self.GAME.start_player = self.GAME.current_player

                    # 기보 추가
                    self.GAME.gibo[self.GAME.round] = []
                    for i in range(0, 5):
                        self.GAME.gibo[self.GAME.round].append(self.board.FACE_CARDS[i])
                    self.GAME.roundwinner.append(self.GAME.start_player)

                    # 노티
                    self.GAME.notice_player[self.GAME.current_player] = "win"
                    self.render()
                    self.GAME.notice_player = {}

                    # 점수 계산
                    tmp_pointcards = []
                    if self.GAME.current_player in self.board.POINT_CARDS:
                        tmp_pointcards = self.board.POINT_CARDS[self.GAME.current_player]

                    tmp_pointcards.extend(Rules.get_point(self.board.FACE_CARDS))
                    self.board.POINT_CARDS[self.GAME.current_player] = copy.deepcopy(tmp_pointcards)

                    # 결과 출력
                    print("\n[round %d] winner %sth player get %d points : %s" %
                          (self.GAME.round,
                           self.GAME.current_player,
                           len(Rules.get_point(self.board.FACE_CARDS)),
                           ",".join(Rules.get_point(self.board.FACE_CARDS))))
                    print("\tface cards ", end=":")
                    print(self.board.FACE_CARDS)
                    print("\twinner card", end=":")
                    print(self.board.FACE_CARDS[self.GAME.current_player])
                    print("\n\n")

                    # 라운드 초기화
                    # TODO self.board.move
                    self.board.FACE_CARDS = {}
                    self.GAME.round += 1
                    self.GAME.jokercall = False
                    self.GAME.round_suit = ""
                    info["turn"] = self.GAME.start_player

                    # 마지막 라운드면 점수 계산 후 종료
                    game_score = 0
                    if self.GAME.round == 11:
                        # 프렌드 없으면 주공이 프렌드
                        if self.GAME.friend_player == "":
                            self.GAME.friend_player = self.GAME.president_player

                        point = 20
                        for agent_uid in self.board.POINT_CARDS:
                            if agent_uid != self.GAME.president_player._uid:
                                if agent_uid != self.GAME.friend_player._uid:
                                    point -= len(self.board.POINT_CARDS[agent_uid])

                        if point >= self.GAME.contract:
                            # 여당(declarer's team) 승리점수 =
                            # (공약 장수(contract) - 14) × 2 + (여당(declarer's team) 획득장수 - 공약 장수(bid))
                            game_score = (self.GAME.contract - 14)*2 + (point - self.GAME.contract)
                            # 주공은 +2*point, 프렌드는 +1*point, 야당은 -1*point
                            for agent_uid in range(0, 5):
                                yadang = True
                                if agent_uid not in self.GAME.point:
                                    self.GAME.point[agent_uid] = 0  # 초기화
                                if agent_uid == self.GAME.president_player._uid:
                                    self.GAME.point[agent_uid] = self.GAME.point[agent_uid] + 2 * game_score
                                    self.GAME.notice_player[agent_uid] = "+%d" % (2 * game_score)
                                    yadang = False
                                if agent_uid == self.GAME.friend_player._uid:
                                    self.GAME.point[agent_uid] = self.GAME.point[agent_uid] + game_score
                                    self.GAME.notice_player[agent_uid] = "+%d" % (game_score)
                                    yadang = False
                                if agent_uid == self.GAME.president_player._uid:
                                        if agent_uid == self.GAME.friend_player._uid:  # 노프렌드
                                            self.GAME.point[agent_uid] = self.GAME.point[agent_uid] + game_score
                                            self.GAME.notice_player[agent_uid] = "+%d" % (4 * game_score)
                                            yadang = False
                                if yadang:
                                    self.GAME.point[agent_uid] = self.GAME.point[agent_uid] - game_score
                                    self.GAME.notice_player[agent_uid] = "-%d" % (game_score)
                        else:
                            # 야당(defenders) 승리점수 = (공약 장수(contract) - 여당(declarer's team) 획득장수)
                            game_score = self.GAME.contract - point
                            # 주공은 -2*point, 프렌드는 -1*point, 야당은 +1*point
                            for agent_uid in range(0, 5):
                                yadang = True
                                if agent_uid not in self.GAME.point:
                                    self.GAME.point[agent_uid] = 0
                                if agent_uid == self.GAME.president_player._uid:
                                    self.GAME.point[agent_uid] = self.GAME.point[agent_uid] - 2 * game_score
                                    self.GAME.notice_player[agent_uid] = "-%d" % (2 * game_score)
                                    yadang = False
                                if agent_uid == self.GAME.friend_player._uid:
                                    self.GAME.point[agent_uid] = self.GAME.point[agent_uid] - game_score
                                    self.GAME.notice_player[agent_uid] = "-%d" % (game_score)
                                    yadang = False
                                # 노프렌드
                                if agent_uid == self.GAME.president_player._uid:
                                    if agent_uid == self.GAME.friend_player._uid:
                                        self.GAME.point[agent_uid] = self.GAME.point[agent_uid] - game_score
                                        self.GAME.notice_player[agent_uid] = "-%d" % (4 * game_score)
                                        yadang = False
                                if yadang:
                                    self.GAME.point[agent_uid] = self.GAME.point[agent_uid] + game_score
                                    self.GAME.notice_player[agent_uid] = "+%d" % (game_score)
                            game_score = -game_score
                        self.GAME.status = Constants.status_done
                        print("[end game]")
                        print("\tpresident : " + self.GAME.president_player._name)
                        print("\tfriend    : " + self.GAME.friend_player._name)
                        print("\tpoint     : %d " % (point))
                        print("\tbid  : %d " % (self.GAME.contract))
                        if point >= self.GAME.contract:
                            print("\tresult   : win")
                            self.GAME.notice = "WIN"
                        else:
                            print("\tresult   : lose")
                            self.GAME.notice = "@LOSE"  # @로 시작하면 render() 함수에서 white style로 변환함

                        # notice
                        self.GAME.notice += "\n%s - %s" \
                                            "\npoint/bid: %d/%d" \
                                            "\nscore: %d" \
                                            % (self.GAME.president_player._name,
                                               self.GAME.friend_player._name,
                                               point,
                                               self.GAME.contract,
                                               game_score)

                        self.render(GAME_END_TIME)
                        self.GAME.notice = ""

                        # score
                        print("\ttotal point : ", end="")
                        print(self.GAME.point)

                        self.done = True

                        # 플레이모드 체크(game)
                        if self.graphics.btnset.PLAYMODE == Constants.playmode_game:
                            self.graphics.btnset.PLAYMODE = Constants.playmode_pause
                    # 플레이모드 체크(round)
                    if self.graphics.btnset.PLAYMODE == Constants.playmode_round:
                        self.graphics.btnset.PLAYMODE = Constants.playmode_pause

            else:
                pass
        else:
            raise "Not Implemented" + self.GAME.status
        self.graphics.checkPLAYMODE()

        return self.getObs(), point, self.done, info

    # 보드, 게임 변수 초기화
    def reset(
        self,
    ) -> Dict:
        """Reset all variables and initialize new game.

        Returns:
            obs: Information about positions of pieces.
        """
        players = copy.deepcopy(self.GAME.players)
        self.board = Board()
        self.GAME = Constants.GAME()
        self.GAME.players = players
        self.GAME.bidder = [0, 1, 2, 3, 4]
        self.GAME.status = Constants.status_bidding
        self.GAME.gibo = {}
        self.GAME.roundwinner = []
        self.GAME.notice_player = {}

        self.done = False
        return self.getObs()

    # 화면 출력. graphics에서 사용할 보드, 게임 변수를 param 으로 작성 및 전달
    def render(
        self,
        wait=RENDER_TIME,
    ) -> None:
        """Display current state of board.

        Returns:
            None
        """

        """
        ##example##
        param = {}

        param["agent"] = {0: "agent1", 1: "agent2", 2: "agent3", 3: "agent4", 4: "agent5"}
        param["handcard"] = {0: ["s-1", "s-2", "s-3", "s-4", "s-5", "s-6", "s-7", "s-j", "s-q", "s-k"],
                             1: ["d-1", "d-2", "d-3", "d-4", "d-5", "d-6", "d-7", "d-j", "d-q", "d-k"],
                             2: ["c-1", "c-2", "c-3", "c-4", "c-5", "c-6", "c-7", "c-j", "c-q", "c-k"],
                             3: ["h-1", "h-2", "h-3", "h-4", "h-5", "h-6", "h-7", "h-j", "h-q"],
                             4: ["s-8", "s-9", "s-0", "d-8", "d-9", "d-0", "h-8", "h-9", "h-0", "c-0"]}

        param["backcard"] = ["c-8", "c-9", "c-0"]
        param["facecard"] = {0: "", 1: "", 2: "", 3: "", 4: ""}
        param["contract"] = {}
        param["notice_player"] = {}
        param["pointcard"] = {}
        """

        param = {}

        # agent
        param[Constants.param_agent] = {}
        for i in range(0, 5):
            player_name = ""
            # 주공, 친구 표시
            player_name = self.GAME.players[i]

            param[Constants.param_agent][i] = player_name

        # handcard
        param[Constants.param_handcard] = {}
        for i in range(0, 5):
            handcard = self.board.PLAYER_CARDS[i]
            if len(handcard) != 0:
                # 카드 소팅
                param[Constants.param_handcard][i] = self.board.PLAYER_CARDS[i]
            else:
                param[Constants.param_handcard][i] = []

        # handcard_sel
        param[Constants.param_handcard_sel] = copy.deepcopy(self.board.SELECTED_CARD)

        # backcard
        param[Constants.param_backcard] = []
        backcard = self.board.BONUS_CARDS
        if len(backcard) != 0:
            param[Constants.param_backcard] = backcard

        # facecard
        param[Constants.param_facecard] = {}
        for i in range(0, 5):
            facecard = self.board.FACE_CARDS
            if i in facecard:
                param[Constants.param_facecard][i] = facecard[i]

        # contract
        if self.GAME.status == Constants.status_play or self.GAME.status == Constants.status_done:
            param[Constants.param_contract] = [self.GAME.president_player._uid,
                                               self.GAME.giruda,
                                               str(self.GAME.contract),
                                               self.GAME.friend_card]

        # notice
        param[Constants.param_notice] = self.GAME.notice
        if len(self.GAME.notice) != 0 and self.GAME.notice[0] == "@":  # notice with white background
            param[Constants.param_notice] = [self.GAME.notice[1:], "white"]

        # score
        param[Constants.param_score] = []
        for i in range(0, 5):
            point = 0
            if i in self.GAME.point:
                point = self.GAME.point[i]
            param[Constants.param_score].append(point)

        # notice_player
        param[Constants.param_notice_player] = {}
        for i in range(0, 5):
            if i in self.GAME.notice_player:
                bidding = self.GAME.notice_player[i]
                param[Constants.param_notice_player][i] = bidding

                """
                if bidding == None:
                    param[Constants.param_notice_player][i] = "pass"
                elif len(bidding) == 2:
                    param[Constants.param_notice_player][i] = "%s%d" % (bidding[1],bidding[0])
                else:
                    param[Constants.param_notice_player][i] = bidding
                """
        # pointcard
        param[Constants.param_pointcard] = {}
        for i in range(0, 5):
            if i in self.board.POINT_CARDS:
                pointcard = self.board.POINT_CARDS[i]
                if len(pointcard) != 0:
                    param[Constants.param_pointcard][i] = self.board.POINT_CARDS[i]

        # gibo
        if len(self.GAME.roundwinner) != 0:
            param[Constants.param_gibo] = self.GAME.gibo
            param[Constants.param_roundwinner] = self.GAME.roundwinner

        self.graphics.update(param)
        self.graphics.setVisible(True)
        loop = QEventLoop()
        QTimer.singleShot(wait, loop.quit)
        loop.exec_()

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

    def close(
        self,
    ) -> None:
        pass

    def getObs(self):
        obs = {}
        obs["board"] = self.board
        obs["game"] = self.GAME
        return obs
