"""
Jeongwon Lee, madlymissyou@gmail.com
seoulai.com
2018
"""
# -*- coding: utf-8 -*-
import sys
import re
import os
import platform

from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QEventLoop

from seoulai_gym.envs.mighty.base import Constants


"""
--------------------------------------------------------------------------

                 handcard[2]                  handcard[3]
LOGO title                                                      credit
                    |---pointcard[2]-- pointcard[3]---|
                    |                                 |
                    |                                 |
  handcard[1]   pointcard[1]       BOARD      pointcard[4]   handcard[4]
                    |                                 |
                    |                       backcard  |
                    |---------  pointcard[0] ---------|

 ContractBoard |           |     handcard[0]
---------------| GiboBoard |                                   MenuBoard
   ScoreBoard  |           |

--------------------------------------------------------------------------
"""

ui_path = os.path.dirname(os.path.abspath(__file__))
form_class = uic.loadUiType(os.path.join(ui_path, "resource/graphics.ui"))[0]


class Graphics(QMainWindow, form_class):
    # 카드 그림파일 폴더
    imgpath = ""
    if platform.system() == "Windows":
        imgpath = os.path.join(ui_path, "resource\\")
    elif platform.system() == "Darwin" or "Linux":
        imgpath = os.path.join(ui_path, "resource/")

    # PRESET
    header_height = 0
    board_width = 450
    board_height = 300
    card_width = 110
    card_height = (card_width * 252 / 182) * 0.95
    card_interval = 30
    card_margin_w = 50
    card_margin_h = 40
    bidding_width = 120
    bidding_height = 40
    notice_width = 120
    notice_height = 40
    playername_width = 260
    playername_height = 30
    bonuscard_width = 80
    bonuscard_height = (bonuscard_width * 252 / 182) * 0.93
    bonuscard_offset = 20
    bonuscard_interval = 20
    facecard_width = 80
    facecard_height = (facecard_width * 252 / 182) * 0.93
    backcard_width = 45
    backcard_height = (backcard_width * 252 / 182) * 0.95
    pointcard_width = 45
    pointcard_height = (pointcard_width * 252 / 182) * 0.95
    pointcard_interval = 15
    credit_width = 200
    credit_height = 130

    handcard_style = "background-color: rgb(247,247,247); border: 1px inset black; border-radius: 8px; padding: 3px"
    notice_white_style = "background-color: rgb(255,255,255); border: 1px inset black; border-radius: 8px; padding: 3px"
    notice_yellow_style = "background-color: rgb(250,223,50); border: 1px inset black; border-radius: 8px; padding: 3px"
    bonuscard_style = "background-color: rgb(247,247,247); border: 1px inset black; border-radius: 4px; padding: 1px"
    pointcard_style = "background-color: rgb(247,247,247); border: 1px inset black; border-radius: 3px; padding: 1px"
    backcard_style = "background-color: rgb(247,247,247); border: 1px inset gray; border-radius: 3px; padding: 2px"
    facecard_style = "background-color: rgb(247,247,247); border: 1px inset black; border-radius: 5px; padding: 3px"
    playername_style = "background-color: rgb(255,255,255);"

    PLAYMODE = Constants.playmode_pause

    AGENTNAME = {0: [], 1: [], 2: [], 3: [], 4: []}
    NOTICE_PLAYER = {0: [], 1: [], 2: [], 3: [], 4: []}
    HANDCARDS = {0: [], 1: [], 2: [], 3: [], 4: []}
    FACECARDS = {0: [], 1: [], 2: [], 3: [], 4: []}
    POINTCARDS = {0: [], 1: [], 2: [], 3: [], 4: []}
    BACKCARDS = []
    NOTICE = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.PLAYMODE = Constants.playmode_pause

        self.initBoard()
        self.initDashboard()
        self.initMenuboard()

        # 카드/텍스트박스 자리 배치
        self.initAgentName()
        self.initBackcard()
        self.initPointcard()
        self.initFacecard()
        self.initHandcard()
        self.initNoticePlayer()
        self.initNotice()

    def initBoard(self):
        # 바탕색
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # Logo
        labelLogo = QLabel(self)
        labelLogo.setGeometry(QtCore.QRect(20, 50, 90, 90))
        pixmap = QPixmap(self.imgpath + "logo.png")
        pixmap_resize = pixmap.scaled(labelLogo.width(), labelLogo.height(), QtCore.Qt.KeepAspectRatio,
                                      QtCore.Qt.SmoothTransformation)
        labelLogo.setPixmap(pixmap_resize)

        # Title
        labelTitle = QLabel(self)
        labelTitle.setText("Sonte Carlo")
        labelTitle.setGeometry(QtCore.QRect(110, 100, 165, 45))
        labelTitle.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        if platform.system() == "Windows":
            labelTitle.setFont(QtGui.QFont("Tahoma", 24))
        elif platform.system() == "Darwin" or "Linux":
            labelTitle.setFont(QtGui.QFont("Tahoma", 28))

        # Subtitle
        labelSubTitle = QLabel(self)
        labelSubTitle.setText("마이티의 정석")
        labelSubTitle.setGeometry(QtCore.QRect(110, 80, 165, 25))
        labelSubTitle.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        if platform.system() == "Windows":
            labelSubTitle.setFont(QtGui.QFont("맑은 고딕", 12))
        elif platform.system() == "Darwin" or "Linux":
            labelSubTitle.setFont(QtGui.QFont("맑은 고딕", 16))

        # Credit
        self.creditLabel = QLabel(self)
        pos_x = self.frame.width() / 2 + self.board_width / 2 + self.card_margin_w
        pos_x = pos_x + self.card_interval * 10 + self.card_width - self.credit_width
        pos_y = self.header_height + self.frame.height() / 2 - self.board_height / 2 - self.card_margin_h
        pos_y = pos_y - self.card_height / 2 - self.credit_height / 2
        self.creditLabel.setGeometry(QtCore.QRect(
            pos_x,
            pos_y,
            self.credit_width,
            self.credit_height))
        creditBoard = CreditBoard(self.creditLabel)
        creditBoard.show()

        # GAMEBOARD
        self.gameboard = QLabel(self.frame)
        self.gameboard.setGeometry(QtCore.QRect(self.frame.width() / 2 - self.board_width / 2,
                                                self.header_height + self.frame.height() / 2 - self.board_height / 2,
                                                self.board_width,
                                                self.board_height))
        self.gameboard.setStyleSheet("background-color: rgb(83, 160, 100); border-radius: 20px;")

    def checkPLAYMODE(self):
        while self.btnset.PLAYMODE == Constants.playmode_pause:
            loop = QEventLoop()
            QTimer.singleShot(10, loop.quit)
            loop.exec_()

    def initAgentName(self):
        pos_0_y = self.header_height + self.frame.height() / 2 + self.board_height / 2 + self.card_margin_h
        pos_1_x = self.frame.width() / 2 - self.board_width / 2 - self.card_margin_w
        pos_1_x = pos_1_x - self.card_width - self.card_interval * 9
        pos_2_y = self.header_height + self.frame.height() / 2 - self.board_height / 2
        pos_2_y = pos_2_y - self.card_margin_h - self.card_height
        pos_3_y = self.header_height + self.frame.height() / 2 - self.board_height / 2
        pos_3_y = pos_3_y - self.card_margin_h - self.card_height
        rect = {0: QtCore.QRect(self.frame.width() / 2 - self.card_width / 2 - self.card_interval * 4.5,
                                pos_0_y,
                                self.playername_width,
                                self.playername_height),
                1: QtCore.QRect(pos_1_x,
                                self.header_height + self.frame.height() / 2 - self.card_height / 2,
                                self.playername_width,
                                self.playername_height),
                2: QtCore.QRect(self.frame.width() / 2 - self.card_margin_w - self.card_width - self.card_interval * 9,
                                pos_2_y,
                                self.playername_width,
                                self.playername_height),
                3: QtCore.QRect(self.frame.width() / 2 + self.card_margin_w,
                                pos_3_y,
                                self.playername_width,
                                self.playername_height),
                4: QtCore.QRect(self.frame.width() / 2 + self.board_width / 2 + self.card_margin_w,
                                self.header_height + self.frame.height() / 2 - self.card_height / 2,
                                self.playername_width,
                                self.playername_height)}
        for i in range(0, 5):
            newcard = QLabel(self.frame)
            newcard.setGeometry(rect[i])
            if i == 0:
                newcard.move(newcard.pos() + QtCore.QPoint(10, self.card_height))
            else:
                newcard.move(newcard.pos() + QtCore.QPoint(10, -30))
            # newcard.move(newcard.pos() + QtCore.QPoint(10, self.card_height))
            newcard.setStyleSheet(self.playername_style)
            newcard.setVisible(True)
            self.AGENTNAME[i] = newcard

    def updateAgentName(self, param):
        for i in range(0, 5):
            self.AGENTNAME[i].setText(str(param[Constants.param_agent][i]))

    # Handcard
    def initHandcard(self):
        pos_1_x = self.frame.width() / 2 - self.board_width / 2 - self.card_margin_w
        pos_1_x = pos_1_x - self.card_width - self.card_interval * 9
        pos_2_y = self.header_height + self.frame.height() / 2 - self.board_height / 2
        pos_2_y = pos_2_y - self.card_margin_h - self.card_height
        pos_3_y = self.header_height + self.frame.height()/2 - self.board_height/2
        pos_3_y = pos_3_y - self.card_margin_h - self.card_height
        rect = {0: QtCore.QRect(self.frame.width() / 2 - self.card_width / 2 - self.card_interval * 4.5,
                                self.header_height+self.frame.height()/2+self.board_height/2 + self.card_margin_h,
                                self.card_width,
                                self.card_height),
                1: QtCore.QRect(pos_1_x,
                                self.header_height + self.frame.height() / 2 - self.card_height / 2,
                                self.card_width,
                                self.card_height),
                2: QtCore.QRect(self.frame.width() / 2 - self.card_margin_w - self.card_width - self.card_interval * 9,
                                pos_2_y,
                                self.card_width,
                                self.card_height),
                3: QtCore.QRect(self.frame.width() / 2 + self.card_margin_w,
                                pos_3_y,
                                self.card_width,
                                self.card_height),
                4: QtCore.QRect(self.frame.width() / 2 + self.board_width / 2 + self.card_margin_w,
                                self.header_height + self.frame.height() / 2 - self.card_height / 2,
                                self.card_width,
                                self.card_height)}

        pos_0_y = self.header_height + self.frame.height() / 2 + self.board_height / 2
        pos_0_y = pos_0_y + self.card_margin_h - self.bonuscard_offset
        pos_1_x = self.frame.width() / 2 - self.board_width / 2 - self.card_margin_w
        pos_1_x = pos_1_x - self.card_width + self.card_interval
        pos_2_y = self.header_height + self.frame.height()/2 - self.board_height/2
        pos_2_y = pos_2_y - self.card_margin_h-self.card_height - self.bonuscard_offset
        pos_3_y = self.header_height + self.frame.height() / 2 - self.board_height/2
        pos_3_y = pos_3_y - self.card_margin_h-self.card_height - self.bonuscard_offset
        rect_bonus = {0: QtCore.QRect(self.frame.width() / 2 - self.card_width / 2 + self.card_interval * 5.5,
                                      pos_0_y,
                                      self.bonuscard_width,
                                      self.bonuscard_height),
                      1: QtCore.QRect(pos_1_x,
                                      self.header_height+self.frame.height()/2-self.card_height/2-self.bonuscard_offset,
                                      self.bonuscard_width,
                                      self.bonuscard_height),
                      2: QtCore.QRect(self.frame.width()/2 - self.card_margin_w - self.card_width + self.card_interval,
                                      pos_2_y,
                                      self.bonuscard_width,
                                      self.bonuscard_height),
                      3: QtCore.QRect(self.frame.width() / 2 + self.card_margin_w + self.card_interval * 10,
                                      pos_3_y,
                                      self.bonuscard_width,
                                      self.bonuscard_height),
                      4: QtCore.QRect(self.frame.width()/2+self.board_width/2+self.card_interval*10+self.card_margin_w,
                                      self.header_height+self.frame.height()/2-self.card_height/2-self.bonuscard_offset,
                                      self.bonuscard_width,
                                      self.bonuscard_height)}

        for i in range(0, 5):
            for n in range(0, 13):
                newcard = QLabel(self.frame)
                if n < 10:
                    newcard.setGeometry(rect[i])
                    newcard.move(newcard.pos() + QtCore.QPoint(self.card_interval * n, 0))
                    newcard.setStyleSheet(self.handcard_style)
                    newcard.setPixmap(QPixmap(self.imgpath + "bck").scaled(self.card_width,
                                                                           self.card_height,
                                                                           QtCore.Qt.KeepAspectRatio,
                                                                           QtCore.Qt.SmoothTransformation))
                    newcard.setVisible(True)
                else:
                    newcard.setGeometry(rect_bonus[i])
                    newcard.move(newcard.pos() + QtCore.QPoint(self.bonuscard_interval * (n-10), 0))
                    newcard.setStyleSheet(self.bonuscard_style)
                    newcard.setPixmap(QPixmap(self.imgpath + "bck").scaled(self.bonuscard_width,
                                                                           self.bonuscard_height,
                                                                           QtCore.Qt.KeepAspectRatio,
                                                                           QtCore.Qt.SmoothTransformation))
                    newcard.setVisible(False)

                self.HANDCARDS[i].append(newcard)

    def updateHandcard(self, param):
        pos_0_y = self.header_height + self.frame.height() / 2 + self.board_height / 2 + self.card_margin_h
        pos_1_x = self.frame.width()/2 - self.board_width/2 - self.card_margin_w
        pos_1_x = pos_1_x - self.card_width - self.card_interval*9
        pos_2_y = self.header_height + self.frame.height()/2 - self.board_height/2
        pos_2_y = pos_2_y - self.card_margin_h - self.card_height
        pos_3_y = self.header_height + self.frame.height()/2 - self.board_height/2
        pos_3_y = pos_3_y - self.card_margin_h - self.card_height
        rect = {0: QtCore.QRect(self.frame.width() / 2 - self.card_width / 2 - self.card_interval * 4.5,
                                pos_0_y,
                                self.card_width,
                                self.card_height),
                1: QtCore.QRect(pos_1_x,
                                self.header_height + self.frame.height() / 2 - self.card_height / 2,
                                self.card_width,
                                self.card_height),
                2: QtCore.QRect(self.frame.width() / 2 - self.card_margin_w - self.card_width - self.card_interval * 9,
                                pos_2_y,
                                self.card_width,
                                self.card_height),
                3: QtCore.QRect(self.frame.width() / 2 + self.card_margin_w,
                                pos_3_y,
                                self.card_width,
                                self.card_height),
                4: QtCore.QRect(self.frame.width() / 2 + self.board_width / 2 + self.card_margin_w,
                                self.header_height + self.frame.height() / 2 - self.card_height / 2,
                                self.card_width,
                                self.card_height)}
        for i in range(0, 5):
            for n in range(0, 13):
                handcard = self.HANDCARDS[i][n]
                if n < 10:
                    handcard.setGeometry(rect[i])
                    handcard.move(handcard.pos() + QtCore.QPoint(self.card_interval * n, 0))

                if n < len(param[Constants.param_handcard][i]):
                    if i in param[Constants.param_handcard_sel]:
                        if n == param[Constants.param_handcard_sel][i]:
                            handcard.move(handcard.pos() + QtCore.QPoint(0, -20))
                    card = param[Constants.param_handcard][i][n]
                    if n < 10:
                        handcard.setPixmap(QPixmap(self.imgpath + card).scaled(self.card_width,
                                                                               self.card_height,
                                                                               QtCore.Qt.KeepAspectRatio,
                                                                               QtCore.Qt.SmoothTransformation))
                    else:
                        handcard.setPixmap(QPixmap(self.imgpath + card).scaled(self.bonuscard_width,
                                                                               self.bonuscard_height,
                                                                               QtCore.Qt.KeepAspectRatio,
                                                                               QtCore.Qt.SmoothTransformation))
                    handcard.setVisible(True)
                else:
                    handcard.setVisible(False)

    # Notice 텍스트박스 배치
    def initNotice(self):
        label = QLabel(self.frame)
        label.setText("")
        label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        label.setStyleSheet(self.notice_yellow_style)
        if platform.system() == "Windows":
            label.setFont(QtGui.QFont("Tahoma", 14, QtGui.QFont.Bold))
        elif platform.system() == "Darwin" or "Linux":
            label.setFont(QtGui.QFont("Tahoma", 18, QtGui.QFont.Bold))
        label.setVisible(False)
        self.NOTICE = label

    def updateNotice(self, param):

        # 텍스트 라인이 여러 줄일 경우 한 줄씩 가로폭 검사하기 위해
        # white 옵션이 있으면,
        strline = ""
        if isinstance(param[Constants.param_notice], list):
            strline = str(param[Constants.param_notice][0]).split("\n")
        # yellow 디폴트 옵션이면,
        else:
            strline = str(param[Constants.param_notice]).split("\n")

        # notice 텍스트박스의 가로 길이를 글자수에 따라 설정
        minWidth = 120
        maxWidth = 0
        for i in range(len(strline)):
            # (전체글자수-한글수) (한글수) 가로폭 다르게 설정
            # todo : Windows에서 pixel 설정
            w = (len(strline[i])-countHangul(strline[i]))*13 + countHangul(strline[i])*17 + 20
            if w > maxWidth:
                maxWidth = w

        if maxWidth < minWidth:
            maxWidth = minWidth

        if maxWidth > self.board_width-20:
            maxWidth = self.board_width-20

        # 텍스트박스 세로폭 설정
        height = len(strline)*25 + 15

        label = self.NOTICE

        if isinstance(param[Constants.param_notice], list):
            label.setText(str(param[Constants.param_notice][0]))
        else:
            label.setText(str(param[Constants.param_notice]))
        label.setGeometry(QtCore.QRect(self.frame.width() / 2 - maxWidth / 2,
                                       self.header_height + self.frame.height() / 2 - height / 2,
                                       maxWidth,
                                       height))

        # Notice 스타일
        # param["notice]="내용": yellow,
        # param["notice"]=["내용","white"]: white

        # param["notice]가 리스트 형태로 들어오면
        if isinstance(param[Constants.param_notice], list):
            if param["notice"][1] == "yellow":
                label.setStyleSheet(self.notice_yellow_style)
            elif param[Constants.param_notice][1] == "white":
                label.setStyleSheet(self.notice_white_style)
        else:
            label.setStyleSheet(self.notice_yellow_style)

        if len(param[Constants.param_notice]) != 0:
            label.setVisible(True)
        else:
            label.setVisible(False)

    # Bidding
    def initNoticePlayer(self):
        pos_0_y = self.header_height + self.frame.height() / 2 + self.board_height / 2 + self.card_margin_h
        pos_1_x = self.frame.width()/2 - self.board_width/2 - self.card_margin_w
        pos_1_x = pos_1_x - self.card_width - self.card_interval*9
        pos_2_y = self.header_height + self.frame.height()/2 - self.board_height/2
        pos_2_y = pos_2_y - self.card_margin_h - self.card_height
        pos_3_y = self.header_height + self.frame.height()/2 - self.board_height/2
        pos_3_y = pos_3_y - self.card_margin_h - self.card_height
        rect = {0: QtCore.QRect(self.frame.width() / 2 - self.card_width / 2 - self.card_interval * 4.5,
                                pos_0_y,
                                self.bidding_width,
                                self.bidding_height),
                1: QtCore.QRect(pos_1_x,
                                self.header_height + self.frame.height() / 2 - self.card_height / 2,
                                self.bidding_width,
                                self.bidding_height),
                2: QtCore.QRect(self.frame.width() / 2 - self.card_margin_w - self.card_width - self.card_interval * 9,
                                pos_2_y,
                                self.bidding_width,
                                self.bidding_height),
                3: QtCore.QRect(self.frame.width() / 2 + self.card_margin_w,
                                pos_3_y,
                                self.bidding_width,
                                self.bidding_height),
                4: QtCore.QRect(self.frame.width() / 2 + self.board_width / 2 + self.card_margin_w,
                                self.header_height + self.frame.height() / 2 - self.card_height / 2,
                                self.bidding_width,
                                self.bidding_height)}

        for i in range(0, 5):
            newcard = QLabel(self.frame)
            newcard.setText("Pass")
            newcard.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            if platform.system() == "Windows":
                newcard.setFont(QtGui.QFont("Tahoma", 14, QtGui.QFont.Bold))
            elif platform.system() == "Darwin" or "Linux":
                newcard.setFont(QtGui.QFont("Tahoma", 18, QtGui.QFont.Bold))
            newcard.setGeometry(rect[i])
            newcard.move(newcard.pos() + QtCore.QPoint(self.card_interval * 6.5 - self.bidding_width / 2,
                                                       self.card_height / 2 - self.bidding_height / 2))
            newcard.setVisible(False)
            self.NOTICE_PLAYER[i] = newcard

    def updateNoticePlayer(self, param):

        for i in range(0, 5):
            self.NOTICE_PLAYER[i].setVisible(False)

        for i in range(0, 5):
            card = self.NOTICE_PLAYER[i]
            if i in param[Constants.param_notice_player]:
                card.setText(str(param[Constants.param_notice_player][i]))
                if param[Constants.param_notice_player][i] == "pass":
                    card.setStyleSheet(self.notice_white_style)
                elif param[Constants.param_notice_player][i][0] == "-":
                    card.setStyleSheet(self.notice_white_style)
                else:
                    card.setStyleSheet(self.notice_yellow_style)
                card.setVisible(True)
            else:
                card.setVisible(False)

    # Backcard
    def initBackcard(self):
        for i in range(0, 3):
            newcard = QLabel(self.frame)
            pos_x = self.frame.width()/2 + self.board_width/2 - self.backcard_width * 3 + self.backcard_width / 2 * i
            pos_y = self.header_height + self.frame.height() / 2 + self.board_height / 2 - self.backcard_height - 10
            newcard.setGeometry(QtCore.QRect(pos_x,
                                             pos_y,
                                             self.backcard_width,
                                             self.backcard_height))
            newcard.setStyleSheet(self.backcard_style)
            newcard.setPixmap(QPixmap(self.imgpath + "bck").scaled(self.backcard_width,
                                                                   self.backcard_height,
                                                                   QtCore.Qt.KeepAspectRatio,
                                                                   QtCore.Qt.SmoothTransformation))
            newcard.setVisible(True)
            self.BACKCARDS.append(newcard)

    def updateBackcard(self, param):
        for i in range(0, 3):
            backcard = self.BACKCARDS[i]
            if i < len(param[Constants.param_backcard]):
                card = param[Constants.param_backcard][i]
                backcard.setPixmap(QPixmap(self.imgpath + card).scaled(self.backcard_width,
                                                                       self.backcard_height,
                                                                       QtCore.Qt.KeepAspectRatio,
                                                                       QtCore.Qt.SmoothTransformation))
                backcard.setVisible(True)
            else:
                backcard.setVisible(False)

    # Facecard
    def initFacecard(self):
        pos_y = self.header_height + self.frame.height() / 2 + self.board_height / 2
        rect = {0: QtCore.QRect(self.frame.width() / 2 - self.facecard_width / 2,
                                pos_y - self.facecard_height - 40,
                                self.facecard_width,
                                self.facecard_height),
                1: QtCore.QRect(self.frame.width() / 2 - self.board_width / 2 + 40,
                                self.header_height + self.frame.height() / 2 - self.facecard_height / 2,
                                self.facecard_width,
                                self.facecard_height),
                2: QtCore.QRect(self.frame.width() / 2 - self.facecard_width - 10,
                                pos_y - self.board_height + 40,
                                self.facecard_width,
                                self.facecard_height),
                3: QtCore.QRect(self.frame.width() / 2 + 10,
                                pos_y - self.board_height + 40,
                                self.facecard_width,
                                self.facecard_height),
                4: QtCore.QRect(self.frame.width() / 2 + self.board_width / 2 - self.facecard_width - 40,
                                self.header_height + self.frame.height() / 2 - self.facecard_height / 2,
                                self.facecard_width,
                                self.facecard_height)}

        for i in range(0, 5):
            newcard = QLabel(self.frame)
            newcard.setGeometry(rect[i])
            newcard.setStyleSheet(self.facecard_style)
            newcard.setPixmap(QPixmap(self.imgpath + "bck").scaled(self.facecard_width,
                                                                   self.facecard_height,
                                                                   QtCore.Qt.KeepAspectRatio,
                                                                   QtCore.Qt.SmoothTransformation))
            newcard.setVisible(False)
            self.FACECARDS[i].append(newcard)

    def updateFacecard(self, param):
        for i in range(0, 5):
            facecard = self.FACECARDS[i][0]
            if i in param[Constants.param_facecard]:
                if param[Constants.param_facecard][i] != "":
                    card = param[Constants.param_facecard][i]
                    facecard.setPixmap(QPixmap(self.imgpath + card).scaled(self.facecard_width,
                                                                           self.facecard_height,
                                                                           QtCore.Qt.KeepAspectRatio,
                                                                           QtCore.Qt.SmoothTransformation))
                    facecard.setVisible(True)
                else:
                    facecard.setVisible(False)  # param[Constants.param_facecard] = {0:"s-1",1:"",2:"",3:"",4:""}
            else:
                facecard.setVisible(False)  # param[Constants.param_facecard] = {0:"s-1"}

    def initPointcard(self):
        pos_y = self.header_height + self.frame.height() / 2 + self.board_height / 2 - self.pointcard_height / 2

        rect = {0: QtCore.QRect(self.frame.width() / 2 - self.board_width / 2 + 40,
                                pos_y,
                                self.pointcard_width,
                                self.pointcard_height),
                1: QtCore.QRect(self.frame.width() / 2 - self.board_width / 2 - self.pointcard_width / 2,
                                self.header_height + self.frame.height() / 2 - self.board_height / 2 + 80,
                                self.pointcard_width,
                                self.pointcard_height),
                2: QtCore.QRect(self.frame.width() / 2 - self.board_width / 2 + 40,
                                pos_y - self.board_height,
                                self.pointcard_width,
                                self.pointcard_height),
                3: QtCore.QRect(self.frame.width() / 2 + self.board_width / 2 - 120,
                                pos_y - self.board_height,
                                self.pointcard_width,
                                self.pointcard_height),
                4: QtCore.QRect(self.frame.width() / 2 + self.board_width / 2 - self.pointcard_width / 2,
                                self.header_height + self.frame.height() / 2 - self.board_height / 2 + 80,
                                self.pointcard_width,
                                self.pointcard_height)}
        pointcard_offset = {0: "x", 1: "y", 2: "x", 3: "x", 4: "y"}

        for i in range(0, 5):
            for n in range(0, 20):  # 최대 20장 가능
                newcard = QLabel(self.frame)
                newcard.setGeometry(rect[i])
                if pointcard_offset[i] == "x":
                    newcard.move(newcard.pos() + QtCore.QPoint(self.pointcard_interval * n, 0))
                elif pointcard_offset[i] == "y":
                    newcard.move(newcard.pos() + QtCore.QPoint(0, self.pointcard_interval * n))
                newcard.setStyleSheet(self.pointcard_style)
                newcard.setPixmap(QPixmap(self.imgpath + "bck").scaled(self.pointcard_width,
                                                                       self.pointcard_height,
                                                                       QtCore.Qt.KeepAspectRatio,
                                                                       QtCore.Qt.SmoothTransformation))
                newcard.setVisible(False)
                self.POINTCARDS[i].append(newcard)

    def updatePointcard(self, param):
        for i in range(0, 5):
            for n in range(0, 20):
                pointcard = self.POINTCARDS[i][n]
                if i in param[Constants.param_pointcard]:
                    if n < len(param[Constants.param_pointcard][i]):
                        card = param[Constants.param_pointcard][i][n]
                        pointcard.setPixmap(QPixmap(self.imgpath + card).scaled(self.pointcard_width,
                                                                                self.pointcard_height,
                                                                                QtCore.Qt.KeepAspectRatio,
                                                                                QtCore.Qt.SmoothTransformation))
                        pointcard.setVisible(True)
                    else:
                        pointcard.setVisible(False)
                else:
                    pointcard.setVisible(False)

    def initDashboard(self):
        LT_width = 160
        LT_height = 110
        self.LT = QLabel(self)
        pos_x = self.frame.width() / 2 - self.board_width / 2 - self.card_margin_w
        pos_x = pos_x - self.card_width - self.card_interval * 9 + 10
        pos_y = self.header_height + self.frame.height() / 2 + self.board_height / 2 - self.pointcard_height / 2 - 20
        self.LT.setGeometry(QtCore.QRect(pos_x,
                                         pos_y,
                                         LT_width,
                                         LT_height))
        self.LT.setStyleSheet("background-color: rgb(235,235,235); border-radius: 5px;")
        self.contractBoard = ContractBoard(self.LT)
        self.contractBoard.show()

        LB_width = 160
        LB_height = 160
        self.LB = QLabel(self)
        pos_x = self.frame.width() / 2 - self.board_width / 2 - self.card_margin_w
        pos_x = pos_x - self.card_width - self.card_interval * 9 + 10
        pos_y = self.header_height + self.frame.height() / 2 + self.board_height / 2
        pos_y = pos_y - self.pointcard_height / 2 - 20 + LT_height + 10
        self.LB.setGeometry(QtCore.QRect(pos_x,
                                         pos_y,
                                         LB_width,
                                         LB_height))
        self.LB.setStyleSheet("background-color: rgb(235,235,235); border-radius: 5px;")
        self.scoreBoard = ScoreBoard(self.LB)
        self.scoreBoard.show()

        R_width = 230
        R_height = 280
        self.R = QLabel(self)
        pos_x = self.frame.width() / 2 - self.board_width / 2 - self.card_margin_w
        pos_x = pos_x - self.card_width - self.card_interval * 9
        pos_x = pos_x + 10 + LT_width + 10
        pos_y = self.header_height + self.frame.height() / 2 + self.board_height / 2 - self.pointcard_height / 2 - 20
        self.R.setGeometry(QtCore.QRect(pos_x,
                                        pos_y,
                                        R_width,
                                        R_height))
        self.R.setStyleSheet("background-color: rgb(235,235,235); border-radius: 5px;")
        self.giboBoard = GiboBoard(self.R)
        self.giboBoard.show()

        B_width = 330
        B_height = 70
        self.B = QLabel(self)
        pos_x = self.frame.width() / 2 + self.board_width / 2 + self.card_margin_w + 45
        pos_y = self.header_height + self.frame.height() / 2 + self.board_height / 2 + self.card_margin_h
        self.B.setGeometry(QtCore.QRect(pos_x,
                                        pos_y,
                                        B_width,
                                        B_height))
        self.B.setStyleSheet("background-color: rgb(235,235,235); border-radius: 5px;")
        self.btnset = ButtonSet(self.B)
        self.btnset.show()

    def updateContract(self, param):
        self.contractBoard.updateContract(param)

    def updateScore(self, param):
        self.scoreBoard.updateScore(param)

    def updateAgent(self, param):
        self.updateAgentName(param)
        self.scoreBoard.updateAgentName(param)

    def updateGibo(self, param):
        self.giboBoard.updateGibo(param)

    def refresh(self):
        self.contractBoard.refreshContract()
        self.giboBoard.refreshGibo()

    def initMenuboard(self):
        B_width = 330
        B_height = 70
        self.M = QLabel(self)
        pos_x = self.frame.width() / 2 + self.board_width / 2 + self.card_margin_w + 45 + 190
        pos_y = self.header_height + self.frame.height() / 2 + self.board_height / 2 + self.card_margin_h + 80
        self.M.setGeometry(QtCore.QRect(pos_x,
                                        pos_y,
                                        B_width-190, B_height))
        self.M.setStyleSheet("background-color: rgb(235,235,235); border-radius: 5px;")
        self.menubtnset = MenuButtonSet(self.M)
        self.menubtnset.show()

    def update(self, param):
        self.refresh()
        if "agent" in param:
            self.updateAgent(param)
        if "score" in param:
            self.updateScore(param)
        if Constants.param_backcard in param:
            self.updateBackcard(param)
        if Constants.param_pointcard in param:
            self.updatePointcard(param)
        if Constants.param_facecard in param:
            self.updateFacecard(param)
        if Constants.param_handcard in param:
            self.updateHandcard(param)
        if Constants.param_notice_player in param:
            self.updateNoticePlayer(param)
        if "notice" in param:
            self.updateNotice(param)
        if "contract" in param:
            self.updateContract(param)
        if Constants.param_gibo in param:
            self.updateGibo(param)


# End of Graphics class
class CreditBoard(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # layout = QHBoxLayout(self)
        # self.setLayout(layout)

        fontsizeTitle = 0
        fontsizeContent = 0
        if platform.system() == "Windows":
            fontsizeTitle = 12
            fontsizeContent = 9
            fontsizeBottom = 8
        elif platform.system() == "Darwin" or "Linux":
            fontsizeTitle = 16
            fontsizeContent = 13
            fontsizeBottom = 12

        center_gap = 7
        T_width = 200
        T_height = 30
        T = QLabel(self)
        T.setGeometry(0, 0, T_width, T_height)
        T.setStyleSheet("background-color: rgb(235,235,235); border: solid 1px black; border-radius: 5px;")

        T.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        txtT = "만든 사람들"
        T.setText(txtT)
        T.setFont(QtGui.QFont("맑은 고딕", fontsizeTitle))

        BL_width = 115
        BL_height = 65
        BL = QLabel(self)
        BL.setGeometry(0, T_height, BL_width-center_gap, BL_height)
        BL.setStyleSheet("padding-top:3px")
        BL.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        txtBL = "기획/연구/개발<br>디자인/연구/개발<br>마이티 연구"
        BL.setText(txtBL)
        BL.setFont(QtGui.QFont("맑은 고딕", fontsizeContent))

        BR_width = 85
        BR_height = 65
        BR = QLabel(self)
        BR.setGeometry(BL_width, T_height, BR_width, BR_height)
        BR.setStyleSheet("padding-top:3px")
        BR.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        txtBR = "김승현<br>이정원<br>마이티연구회"
        BR.setText(txtBR)
        BR.setFont(QtGui.QFont("맑은 고딕", fontsizeContent))

        B_width = 200
        B_height = 40
        B = QLabel(self)
        B.setGeometry(0, T_height+BL_height, B_width, B_height)
        B.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        txtB = "Since 2018.7.29.<br>kimseunghyun@gmail.com"
        B.setText(txtB)
        B.setFont(QtGui.QFont("맑은 고딕", fontsizeBottom))


class ButtonSet(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        btn = []
        # name = ["Auto\nPlay", "Pause", "|<", "<5","<", ">", "5>", ">|"]
        name = ["Auto\nPlay", "Pause", ">", "5 >", ">|"]
        for i in range(0, 5):
            btn.append(QPushButton(name[i]))
            btn[i].setFixedWidth(50)
            btn[i].setFixedHeight(50)
            btn[i].setFlat(True)
            btn[i].setStyleSheet("background-color: rgb(255,255,255); border-radius: 5px;")
            layout.addWidget(btn[i])

        btn[0].clicked.connect(self.btn0_clicked)
        btn[1].clicked.connect(self.btn1_clicked)
        btn[2].clicked.connect(self.btn2_clicked)
        btn[3].clicked.connect(self.btn3_clicked)
        btn[4].clicked.connect(self.btn4_clicked)

        self.PLAYMODE = Constants.playmode_pause

    def btn0_clicked(self):
        self.PLAYMODE = Constants.playmode_autoplay
        print(self.PLAYMODE)

    def btn1_clicked(self):
        self.PLAYMODE = Constants.playmode_pause
        print(self.PLAYMODE)

    def btn2_clicked(self):
        self.PLAYMODE = Constants.playmode_step
        print(self.PLAYMODE)

    def btn3_clicked(self):
        self.PLAYMODE = Constants.playmode_round
        print(self.PLAYMODE)

    def btn4_clicked(self):
        self.PLAYMODE = Constants.playmode_game
        print(self.PLAYMODE)


class MenuButtonSet(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        btn = []

        name = ["Quit (Ctrl+Q)"]
        for i in range(0, 1):
            btn.append(QPushButton(name[i]))
            btn[i].setFixedWidth(115)
            btn[i].setFixedHeight(50)
            btn[i].setFlat(False)
            btn[i].setStyleSheet("background-color: rgb(255,255,255); border-radius: 5px;")
            layout.addWidget(btn[i])

        btn[0].clicked.connect(self.menubtn0_clicked)

        self.PLAYMODE = Constants.playmode_pause

    def menubtn0_clicked(self):
        print("clicked pb_1")
        qApp.quit()
        sys.exit(0)


class ContractBoard(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        width = 60
        height = 0
        if platform.system() == "Windows":
            height = 19
        elif platform.system() == "Darwin" or "Linux":
            height = 16

        category = ["President", "Giruda", "Contract", "Friend"]
        value = ["", "", "", ""]
        category_label = []
        self.value_label = []
        layout = QGridLayout(self)
        self.setLayout(layout)
        for i in range(0, 4):
            category_label.append(QLabel(category[i]))
            category_label[i].setFixedWidth(width)
            category_label[i].setFixedHeight(height)
            category_label[i].setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            self.value_label.append(QLabel(value[i]))
            self.value_label[i].setFixedWidth(width)
            self.value_label[i].setFixedHeight(height)
            self.value_label[i].setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            layout.addWidget(category_label[i], i, 0)
            layout.addWidget(self.value_label[i], i, 1)

    def updateContract(self, param):
        redcard = "color: rgb(253,112,119)"
        blackcard = "color: rgb(102,102,102)"
        fontsize = "font-size: 18px;"
        if platform.system() == "Windows":
            fontsize = "font-size: 20px;"
        elif platform.system() == "Darwin" or "Linux":
            fontsize = "font-size: 18px;"

        # 주공 president
        presidentUID = param[Constants.param_contract][0]
        self.value_label[0].setText(str(param[Constants.param_agent][presidentUID]))

        # 기루다 giruda
        giruda = param[Constants.param_contract][1]+"-"
        print(giruda)
        self.value_label[1].setText(str(suitSymbol(giruda)))
        # 빨간색 카드이면,
        if giruda[0] == "d" or giruda[0] == "h":
            self.value_label[1].setStyleSheet(fontsize + redcard)
        # 검은색 카드이면
        else:
            self.value_label[1].setStyleSheet(fontsize + blackcard)

        # 공약 bid
        self.value_label[2].setText(str(param[Constants.param_contract][2]))

        # 친구 friend
        # friend = suitSymbol(param[Constants.param_contract][3][0:2])+cardRank(param[Constants.param_contract][3][1:3])
        # self.value_label[3].setText(str(friend))
        self.value_label[3].setText(str(param[Constants.param_contract][3]))

    def refreshContract(self):
        for i in range(0, 4):
            self.value_label[i].setText(".")
            self.value_label[i].setStyleSheet("color: black")


class ScoreBoard(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        width = 60
        height = 0
        if platform.system() == "Windows":
            height = 19
        elif platform.system() == "Darwin" or "Linux":
            height = 16

        playerTitle = QLabel("Player")
        scoreTitle = QLabel("Score")
        playerTitle.setFixedWidth(width)
        playerTitle.setFixedHeight(height)
        scoreTitle.setFixedWidth(width)
        scoreTitle.setFixedHeight(height)
        playerTitle.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        scoreTitle.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        self.playername_label = []
        self.playerscore_label = []

        for i in range(0, 5):
            name = ""
            self.playername_label.append(QLabel(name))
            self.playername_label[i].setFixedWidth(width)
            self.playername_label[i].setFixedHeight(height)
            self.playername_label[i].setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            value = 0
            self.playerscore_label.append(QLabel(str(value)))
            self.playerscore_label[i].setFixedWidth(width)
            self.playerscore_label[i].setFixedHeight(height)
            self.playerscore_label[i].setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        layout = QGridLayout(self)
        layout.addWidget(playerTitle, 0, 0)
        layout.addWidget(scoreTitle, 0, 1)
        for i in range(0, 5):
            layout.addWidget(self.playername_label[i], i+1, 0)
            layout.addWidget(self.playerscore_label[i], i+1, 1)
        self.setLayout(layout)

    def updateScore(self, param):
        for i in range(0, 5):
            self.playerscore_label[i].setText(str(param[Constants.param_score][i]))

    def updateAgentName(self, param):
        for i in range(0, 5):
            player_name = str(param[Constants.param_agent][i])
            # if player_name.find("[주공]") == 0 or player_name.find("[친구]") == 0:
            #     player_name = player_name[5:]
            self.playername_label[i].setText(player_name)


class GiboBoard(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        height = 0
        if platform.system() == "Windows":
            height = 19
        elif platform.system() == "Darwin" or "Linux":
            height = 16

        # title
        width = 28

        self.label = [[QLabel("")] * 6 for i in range(11)]
        layout = QGridLayout(self)
        for r in range(0, 11):
            for c in range(0, 6):
                str = ""
                if r == 0 and c == 0:
                    str = "Rec."
                elif r == 0:
                    str = "P%i" % (c)
                elif c == 0:
                    str = "R%i" % (r)

                self.label[r][c] = QLabel(str)
                self.label[r][c].setFixedWidth(width)
                self.label[r][c].setFixedHeight(height)
                self.label[r][c].setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

                layout.addWidget(self.label[r][c], r, c)

        self.setLayout(layout)

    # 기보 업데이트
    # param[Constants.param_gibo] = {1:["","","","",""],2:[],...}
    # param[Constants.param_roundwinner] = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
    def updateGibo(self, param):
        redcard = "color: rgb(253,112,119);"
        blackcard = "color: rgb(102,102,102);"
        roundwinner = "background-color: rgb(253,235,119); font-weight: bold;"
        startplayer = "border-left: 1px solid #bbb; border-radius: 3px;"

        # Contract가 결정되어야 주공 등의 정보를 참조하여 기보를 업데이트 한다
        if Constants.param_contract in param:

            for c in range(1, 6):  # 기보 가로줄 1-5
                if c-1 == param[Constants.param_contract][0]:
                    self.label[0][c].setStyleSheet("color: rgb(253,112,119); font-weight: bold")
                else:
                    self.label[0][c].setStyleSheet("color: black")

            for r in range(1, 11):  # 기보 세로줄 1-10
                if r in param[Constants.param_gibo]:
                    for c in range(1, 6):  # 기보 가로줄 1-5

                        cardstr = str(param[Constants.param_gibo][r][c-1])
                        cardsymbol = suitSymbol(cardstr[0:2]) + cardRank(cardstr[1:3])
                        self.label[r][c].setText(cardsymbol)

                        style = ""

                        # 빨간색 카드이면,
                        if cardstr[0] == "d" or cardstr[0] == "h":
                            style += redcard
                        # 검은색 카드이면
                        else:
                            style += blackcard

                        # RoundWinner이면, 하이라이트
                        if c-1 == param[Constants.param_roundwinner][r-1]:
                            style += roundwinner

                        # StarPlayer
                        # 1 라운드에서는 주공이 startplayer
                        if r == 1:
                            if c-1 == param[Constants.param_contract][0]:
                                style += startplayer
                        # 2-10라운드에서는, 직전 roundwinner가 startplayer
                        else:
                            if c-1 == param[Constants.param_roundwinner][r-2]:
                                style += startplayer

                        self.label[r][c].setStyleSheet(style)

    def refreshGibo(self):
        for c in range(1, 6):  # 기보 가로줄 1-5
            self.label[0][c].setStyleSheet("color: black")
        for r in range(1, 11):  # 기보 세로줄 1-10
            for c in range(1, 6):  # 기보 가로줄 1-5
                self.label[r][c].setText(".")
                self.label[r][c].setStyleSheet("color: black")


class MenuBoard(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # 배치될 위젯 변수 선언
        self.pb_1 = QPushButton()

        # 레이아웃 선언 및 Form Widget에 설정
        self.layout_1 = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.setLayout(self.layout_1)
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("PushButton Shortcut")

        # 라벨1의 설정 및 레이아웃 추가
        self.pb_1.setText("종료 (Ctrl+Q)")
        self.pb_1.setShortcut("Ctrl+Q")
        self.layout_1.addWidget(self.pb_1)

        self.pb_1.clicked.connect(self.pb_1_clicked)

    # 종료 버튼 누르면, 종료
    def pb_1_clicked(self):
        print("clicked pb_1")
        qApp.quit()
        sys.exit(0)


def show(param, msg="done", time=300):
    loop = QEventLoop()
    QTimer.singleShot(time, loop.quit)
    loop.exec_()

    graphics.update(param)
    graphics.setVisible(True)


def countHangul(text):
    # Check the Python Version
    pyVer3 = sys.version_info >= (3, 0)
    if pyVer3:  # for Ver 3 or later
        encText = text
    """
    else:  # for Ver 2.x
        if type(text) is not unicode:
            encText = text.decode("utf-8")
        else:
            encText = text
    """
    hanCount = 0
    for i in range(len(encText)):
        hanCount += len(re.findall(u"[\u3130-\u318F\uAC00-\uD7A3]+", encText[i]))
    return hanCount


def suitSymbol(x):
    return {
        "s-": "♠",
        "d-": "♦",
        "h-": "♥",
        "c-": "♣",
        "jo": "☆"
    }.get(x, "")


def cardRank(x):
    return {
        "-1": "A",
        "-2": "2",
        "-3": "3",
        "-4": "4",
        "-5": "5",
        "-6": "6",
        "-7": "7",
        "-8": "8",
        "-9": "9",
        "-0": "T",
        "-j": "J",
        "-q": "Q",
        "-k": "K",
        "os": "♠",
        "od": "♦",
        "oh": "♥",
        "oc": "♣"
    }.get(x, "")


def test():
    print("Sonte Carlo")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    graphics = Graphics()
    graphics.resize(QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height())

    test()
    app.exec_()
