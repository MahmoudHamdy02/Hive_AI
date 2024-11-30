from Game_Logic.Piece.Piece import Piece
from Game_Logic.Board.Board import Board
class Spider(Piece):
    def __init__(self, owner, position=None):
        super().__init__(owner, position)

    def getMoves(self, board:Board) -> list:
        """
        Returns a list of all possible moves for the Spider by moving exactly three steps.
        """
        visited = set()  # To track visited positions and prevent loops
        next_positions = [(self.position, [])]  # Track position and path

        for i in range(3):  # Perform exactly 3 steps
            current_positions = []
            for pos, path in next_positions:
                neighbors = board.getNeighbors(pos)
                for neighbor in neighbors:
                    # Check for a common space and ensure the neighbor is not visited
                    common_spaces = board.commonspace(pos, neighbor)
                    if common_spaces:
                        for comm in common_spaces:
                            if comm not in visited:
                                visited.add(comm)
                                current_positions.append((comm, path + [comm]))
            next_positions = current_positions
        #next_positions.pop()
        # Return all unique positions that can be reached in exactly 3 steps
        return [path for pos, path in next_positions]