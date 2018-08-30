"""
Martin Kersner, m.kersner@gmail.com
seoulai.com
2018
"""


class Constants(object):
    """ Constants to share between classes and functions for checkers game.
    """
    EMPTY = 0
    LIGHT = 1
    DARK = 2
    LIGHT_KING = 3
    DARK_KING = 4

    UP = 5
    DOWN = 6


class Piece(object):
    def __init__(self, ptype: int, direction: int):
        self.ptype = ptype
        self.direction = direction
        self._king = False

    def make_king(self):
        self._king = True

    @property
    def king(self):
        return self._king

    def __str__(self):
        return str(self.ptype)

    def direction(self):
        return self.direction


class DarkPiece(Constants, Piece):
    def __init__(self):
        super().__init__(ptype=self.DARK, direction=self.DOWN)


class LightPiece(Constants, Piece):
    def __init__(self):
        super().__init__(ptype=self.LIGHT, direction=self.UP)
