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
        self.positions = []
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
        
    # Position Management
    def add_position(self, position):
        """
        Adds a new position to the player's list of positions.
        """
        self.positions.append(position)

    def remove_position(self, position):
        """
        Removes a position from the player's list of positions.
        """
        if position in self.positions:
            self.positions.remove(position)
        else:
            raise Exception("Position not found in the player's list.")

    def get_positions(self):
        """
        Returns the list of the player's piece positions.
        """
        return self.positions

    def clear_positions(self):
        """
        Clears all positions associated with the player.
        """
        self.positions = []
