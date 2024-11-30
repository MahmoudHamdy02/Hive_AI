import Player, Board

from Player import Color, Player
from Board import  *


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
        for i in range(3):
            next_pos=[]
            list_of_neighbors=[]
            list_of_neighbors=board.getNeighbors(self.position)
            for neighbors in list_of_neighbors:
                comm

        for _ in range(3):
            next_positions = []
            for pos, path in current_positions:
                neighbors = self.getNeighbors(board)
                for neighbor in neighbors:
                    if not board.hasPieceAt(neighbor[0], neighbor[1]) and neighbor not in visited:
                        # Check hive continuity
                        if self.commonspace(Piece(self.owner, neighbor), board):
                            new_path = path + [neighbor]
                            next_positions.append((neighbor, new_path))
                            visited.add(neighbor)
            current_positions = next_positions

        # Collect final valid moves after exactly three steps
        valid_moves = [path[-1] for _, path in current_positions if len(path) == 3]
        return valid_moves

# Create players

# Create a player with WHITE color
player1 = Player(Color.WHITE)

# Create a player with BLACK color
player2 = Player(Color.BLACK)


# Create a board and add some pieces to it
board = Board()
board.addPiece(Piece(player1), 1, 0)  # Piece at (1, 0)
board.addPiece(Piece(player1), 1, 1)  # Piece at (1, 1)
board.addPiece(Piece(player2), 0, 1)  # Piece at (0, 1)
board.addPiece(Piece(player1), -1, 0)  # Piece at (1, 0)
board.addPiece(Piece(player1), -1, 1)  # Piece at (1, 1)
board.addPiece(Piece(player2), -2, 1)  # Piece at (0, 1)

# Add the Spider to the board
spider = Spider(player1, (0, 0))
board.addPiece(spider, 0, 0)

# Get Spider's moves
spider_moves = spider.getMoves(board)

# Print the results
print(f"Spider's starting position: {spider.position}")
print(f"Possible moves for Spider: {spider_moves}")




