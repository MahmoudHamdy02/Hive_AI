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




from Board import Board
from Player import Player, Color

board = Board()
player1 = Player(Color.WHITE)
player2 = Player(Color.BLACK)
grass1 = Spider(player1, (0, 0))
grass2 = Spider(player2, (1, 0))
grass3 = Spider(player1, (0, 1))
grass02 = Spider(player2, (0, 2))
grass20 = Spider(player2, (2, 0))
grass11 = Spider(player1, (1, -1))
grassn_11 = Spider(player1, (-1, 1))
board.addPiece(grass1, 0, 0)
board.addPiece(grass2, 1, 0)
board.addPiece(grass3, 0, 1)
board.addPiece(grass02, 0, 2)
board.addPiece(grass20, 2, 0)
board.addPiece(grass11, 1, -1)
board.addPiece(grassn_11, -1, 1)
print(grass2.getMoves(board))
