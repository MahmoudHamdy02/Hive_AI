import Player, Board

class Piece:
    def __init__(self, owner, position=None):
        """
        Initializes a Generic Hive Piece

        """
        self.owner: Player = owner
        self.position: tuple = position

    def getMoves(self, board: Board) -> list:
        """
        Returns a list of all possible moves for the piece

        """
        raise NotImplementedError("getMoves() must be implemented by subclass")
    
    def move(self, q, r):
        """
        Moves the piece to the specified position

        """
        self.position = (q, r)

class Grasshopper(Piece):
    def __init__(self, owner, position=None):
        """
        Initializes a Grasshopper Piece

        """
        super().__init__(owner, position)

    def getMoves(self, board) -> list:
        """
        Returns a list of all possible moves for the Grasshopper

        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        moves = []
        jumped = False
        if self.position:
            for dq, dr in directions:
                q, r = self.position[0]+dq, self.position[1]+dr
                while board.hasPieceAt(q, r):
                    q, r = q+dq, r+dr
                    jumped = True
                if jumped:
                    moves.append((q, r))
                jumped = False
        return moves
    

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
    
    