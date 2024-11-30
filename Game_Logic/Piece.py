import Player, Board



class Piece:
    def __init__(self, owner, position=None,):
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



class Spider(Piece):
    def __init__(self, owner, position=None):
        super().__init__(owner, position)

    def getMoves(self, board: Board) -> list:
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
      
        return list(final_positions)
