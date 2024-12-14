from Game_Logic.Piece.Piece import Piece

class Ant(Piece):

    def __init__(self, owner, position=None):
        """
        Initializes an Ant Piece
        """
        super().__init__(owner, position)

    # def getMoves(self, board) -> list:
    #     """
    #     Returns a list of all valid moves for the Ant.
        
    #     """

    #     if self.position is None:
    #         return []  
        
        
    #     # ADJACENT_HEXES = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
        
    #     # def get_adjacent_hexes(q, r):
    #     #     return [(q + dq, r + dr) for dq, dr in ADJACENT_HEXES]
    
    #     # board.grid[self.position].removePiece()

    #     # def is_hive_continuous():
    #     #     visited = set()
    #     #     iterator = iter(board.grid.keys())
    #     #     start = next(iterator)  # Get the first hex in the grid
    #     #     while not board.hasPieceAt(*start):
    #     #         start = next(iterator)

    #     #     def dfs(node):
    #     #         visited.add(node)
    #     #         for neighbor in get_adjacent_hexes(*node):
    #     #             if board.hasPieceAt(*neighbor) and neighbor not in visited:
    #     #                 dfs(neighbor)

    #     #     dfs(start)
    #     #     print(len(visited), board.noOfPieces)
    #     #     return len(visited) == board.noOfPieces -1
        
    #     # continuous = is_hive_continuous()
        
    #     # board.addPiece(self, *self.position)

    #     # if not continuous:
    #     #     return []

    #     visited = set()
    #     valid_moves = set()


    #     def dfs(position):
    #         """Depth-first search to find all reachable positions."""

    #         for neighbor in board.getNeighbors(position):
    #             nextPositions = board.commonspace(position, neighbor)
    #             if nextPositions:
    #                 valid_moves.update(nextPositions)
    #                 for pos in nextPositions:
    #                     if pos not in visited:
    #                         visited.add(pos)
    #                         dfs(pos)
        
    #     # Start DFS from the current position
    #     visited.add(self.position)
    #     dfs(self.position)

    #     return list(valid_moves)

    def getMoves(self, board) -> list:
        """
        Returns a list of all valid paths for the Ant.
        Each path is represented as a list of positions.
        """
        if self.position is None:
            return []

        visited = set()
        all_paths = []

        def dfs(position, current_path):
            """Depth-first search to find all valid paths."""
            for neighbor in board.getNeighbors(position):
                nextPositions = board.commonspace(position, neighbor)
                if nextPositions:
                    for pos in nextPositions:
                        if pos not in visited:
                            visited.add(pos)
                            dfs(pos, current_path + [pos])

            # If current_path is non-empty and represents a valid path, add it
            if len(current_path) >= 1:  # A path must have at least 2 positions
                all_paths.append(current_path)

        # Start DFS from the current position
        visited.add(self.position)
        dfs(self.position, [])

        print("Ant's valid moves:", all_paths) 

        return all_paths
