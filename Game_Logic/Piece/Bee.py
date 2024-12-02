from Game_Logic.Piece.Piece import Piece
from Game_Logic.Game.MoveFilter import MoveFilter

class Bee(Piece):
    def __init__(self, owner, position=None):
        """
        Initializes an Ant Piece
        """
        super().__init__(owner, position)

    def getMoves(self, board) -> list:
        """
        
        Returns a list of all possible moves for the Bee.
        
        """
        
        directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
        moves = []
        
        if self.position:
            q, r = self.position
            for dq, dr in directions:
                nq, nr = q + dq, r + dr
                if not board.hasPieceAt(nq, nr):  # The Bee can't move to a square with a piece
                    if MoveFilter.is_it_sliding(self.position, (nq, nr), board):
                        moves.append((nq, nr))

        return moves
