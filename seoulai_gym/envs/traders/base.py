"""
Cinyoung Hur, cinyoung.hur@gmail.com
seoulai.com
2018
"""


class Constants(object):
    """ Constants to share between classes and functions for checkers game.
    """
    BUY = 0
    SELL = 1
    


# class Piece(object):
#     def __init__(self, ptype: int, direction: int):
#         self.ptype = ptype
#         self.direction = direction
#         self.king = False

#     def make_king(self):
#         self.king = True

#     def is_king(self):
#         return self.king

#     def __str__(self):
#         return str(self.ptype)

#     def direction(self):
#         return self.direction


# class DarkPiece(Constants, Piece):
#     def __init__(self):
#         super().__init__(ptype=self.DARK, direction=self.DOWN)


# class LightPiece(Constants, Piece):
#     def __init__(self):
#         super().__init__(ptype=self.LIGHT, direction=self.UP)
