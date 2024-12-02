from Game_Logic.Piece.Piece import Piece

class Bee(Piece):
    def __init__(self)-> None:
        """
        Initializes a Bee Piece.
        The Bee moves one space in any direction.
        """
        super().__init__()

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
                    moves.append((nq, nr))

        return moves
