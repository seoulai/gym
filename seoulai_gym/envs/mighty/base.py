"""
Seung-Hyun Kim, kimseunghyun@gmail.com
seoulai.com
2018
"""


class Constants(object):
    """Constants to share between classes and functions for
    checkers game.
    """
    # status
    status_bidding = "bidding"
    status_choose_card = "choose card"
    status_contract = "contract"
    status_friend = "friend"
    status_play = "play"
    status_done = "done"

    # playmode
    playmode_autoplay = "AUTOPLAY"
    playmode_pause = "PAUSE"
    playmode_step = "STEP"
    playmode_round = "ROUND"
    playmode_game = "GAME"

    # card
    card_mighty = "mighty"
    card_joker = "jok"
    suit_spade = "s"
    suit_diamond = "d"
    suit_clover = "c"
    suit_heart = "h"
    suit_joker = "j"

    # param
    param_agent = "agent"
    param_score = "score"
    param_backcard = "backcard"
    param_pointcard = "pointcard"
    param_facecard = "facecard"
    param_handcard = "handcard"
    param_handcard_sel = "handcard_sel"
    param_notice = "notice"
    param_notice_player = "notice_player"
    param_contract = "contract"
    param_gibo = "gibo"
    param_roundwinner = "roundwinner"
    param_selectedcard = "selectedcard"
    param_friend_card = "friend_card"

    class GAME(object):
        president_player = ""
        friend_player = ""
        giruda = ""
        round_suit = ""
        contract = 0
        friend_card = ""
        point = {}
        mighty_card = "s-1"
        jokercall_card = "c-3"
        status = ""
        bidder = []
        notice_player = {}
        players = []
        round = 1
        start_player = 0
        jokercall = False
        current_player = 0
        notice = ""
        gibo = {}
        roundwinner = []
