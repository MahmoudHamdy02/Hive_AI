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


    def getNeighbors(self, board: Board) -> list:
        """
        Returns a list of all neighboring pieces

        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        neighbors = []
        for dq, dr in directions:
            q, r = self.position[0] + dq, self.position[1] + dr
            if board.hasPieceAt(q, r):
                neighbors.append((q, r))
        return neighbors

    def commonspace(self, piece2,board:Board)->list:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        free_places1=[]
        free_places2=[]
        for dq,dr in directions:
            q, r = self.position[0] + dq, self.position[1] + dr
            if not board.hasPieceAt(q, r):
                free_places1.append((q, r))
        for dq,dr in directions:
            q, r = piece2.position[0] + dq, piece2.position[1] + dr
            if not board.hasPieceAt(q, r):
                free_places2.append((q, r))
        common_positions = list(set(free_places1) & set(free_places2))
        return common_positions






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


