from Game_Logic.Piece.Piece import Piece

class Ant(Piece):

    def __init__(self, owner, position=None):
        """
        Initializes an Ant Piece

        """
        super().__init__(owner, position)

    def getMoves(self, board) -> list:
        """
        Returns a list of all valid moves for the Ant.
        
        """
        if self.position is None:
            return []  

        visited = set()
        valid_moves = set()


        def dfs(position):
            """Depth-first search to find all reachable positions."""

            for neighbor in board.getNeighbors(position):
                nextPositions = board.commonspace(position, neighbor)
                if nextPositions:
                    valid_moves.update(nextPositions)
                    for pos in nextPositions:
                        if pos not in visited:
                            visited.add(pos)
                            dfs(pos)
        
        # Start DFS from the current position
        visited.add(self.position)
        dfs(self.position)

        return list(valid_moves)