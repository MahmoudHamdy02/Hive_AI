from Game_Logic.Piece.Piece import Piece

class Beetle(Piece):
    def __init__(self, owner, position=None):
        """
        Initializes an Ant Piece
        """
        super().__init__(owner, position)

    def getMoves(self, board) -> list:
        """
        Returns a list of all possible moves for the Beetle

        Beetle can move to any adjacent hex tile, including climbing on top of other pieces
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        moves = []
        if self.position:
            q, r = self.position
            for dq, dr in directions:
                nq, nr =  q + dq, r + dr
                moves.append((nq, nr))

        return moves