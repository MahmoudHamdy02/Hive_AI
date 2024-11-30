from Game_Logic.Piece.Piece import Piece

class Ant(Piece):

    def __init__(self, owner, position=None):
        """
        Initializes an Ant Piece

        """
        super().__init__(owner, position)

    def getMoves(self, board) -> list:
        if self.position is None:
            return []

        visited = set()
        valid_moves = set()

        def dfs(position):
            """Depth-first search to find all reachable positions."""
            for neighbor in board.getNeighbors(position):
                print(f"Neighbor: {neighbor}")  # Debugging line
                nextPositions = board.commonspace(position, neighbor)
                print(f"nextPositions: {nextPositions}")  # Debugging line
                if nextPositions:
                    valid_moves.update(nextPositions)
                    for pos in nextPositions:
                        if pos not in visited:
                            print(f"visiting pos: {pos}")  # Debugging line
                            visited.add(pos)
                            dfs(pos)

        visited.add(self.position)
        dfs(self.position)

        return list(valid_moves)
