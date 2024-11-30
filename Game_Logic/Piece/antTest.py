from Game_Logic.Piece.Ant import Ant
from Game_Logic.Board.Board import Board
from Game_Logic.Player.Player import Player, Color

# Initialize the board
board = Board()

# Create players
player1 = Player(Color.WHITE)
player2 = Player(Color.BLACK)

# Create Ant and other pieces
ant = Ant(player1, (0, 0))
piece1 = Ant(player2, (1, 0))  # Blocker on one side
piece2 = Ant(player1, (2, 0))  # Another adjacent piece
piece3 = Ant(player2, (3, 0))  
piece4 = Ant(player2, (4, 0))  
piece5 = Ant(player2, (5, 0))  
# Place pieces on the board
board.addPiece(ant, 0, 0)       # Add the Ant to (0, 0)
board.addPiece(piece1, 1, 0)    # Add a blocking piece at (1, 0)
board.addPiece(piece2, 2, 0)    # Add another piece at (0, 1)
board.addPiece(piece3, 3, 0)    # Add another piece at (0, 1)
board.addPiece(piece4, 4, 0)    # Add another piece at (0, 1)
board.addPiece(piece5, 5, 0)    # Add another piece at (0, 1)


# Test Ant's valid moves
ant_moves = ant.getMoves(board)

print("Ant's valid moves:", ant_moves) 