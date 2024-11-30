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
        visited = set()
        current_positions = [(self.position, [])]  # Track position and path

        init_pos=self.position
        next_pos = [init_pos]
        list_of_neighbors = []
        for i in range(3):
            for pos in next_pos:
                list_of_neighbors=board.getNeighbors(pos)
                for neighbors in list_of_neighbors:
                    next_pos.append(board.commonspace(pos,tuple(neighbors)))



                next_pos.pop()
        return next_pos




