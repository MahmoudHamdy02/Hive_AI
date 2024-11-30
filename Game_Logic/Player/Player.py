from Game_Logic.Player.Color import Color
from  Game_Logic.Piece.PieceType import PieceType

class Player:
    def __init__(self, color: Color):
        self.color = color
        self.remainingPieces = { PieceType.BEE: 1,
                                 PieceType.SPIDER: 2,
                                 PieceType.BEETLE: 2,
                                 PieceType.GRASSHOPPER: 3,
                                 PieceType.ANT: 3 }

    def get_remaining_pieces(self):
        return self.remainingPieces

    def set_remaining_pieces(self, remainingPieces):
        self.remainingPieces = remainingPieces

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def update_remaining_pieces(self, piece_type: PieceType):
        if piece_type in self.remainingPieces and self.remainingPieces[piece_type] > 0:
            self.remainingPieces[piece_type] -= 1
        else:
            raise Exception("Invalid piece type or no remaining pieces of that type")
