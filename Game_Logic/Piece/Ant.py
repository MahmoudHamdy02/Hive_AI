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
            for neighbor in board.get_neighbors(*position):
                if neighbor not in visited and not board.hasPieceAt(*neighbor):

                    neighbors = board.get_neighbors(*neighbor)
                    occupied_neighbors = sum(1 for n in neighbors if board.hasPieceAt(*n))

                    visited.add(neighbor)

                    if (occupied_neighbors <= 3 and occupied_neighbors>0 ):
                        valid_moves.add(neighbor)

                    if occupied_neighbors != 0:
                        dfs(neighbor)
                   

        # Start DFS from the current position
        visited.add(self.position)
        dfs(self.position)

        return list(valid_moves)