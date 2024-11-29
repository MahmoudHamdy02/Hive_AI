from Piece import Grasshopper
from Board import Board
from Player import Player, Color

board = Board()
player1 = Player(Color.WHITE)
player2 = Player(Color.BLACK)
grass1 = Grasshopper(player1, (0,0))
grass2 = Grasshopper(player2, (1,0))
grass3 = Grasshopper(player1, (0,1))
grass02 = Grasshopper(player2, (0,2))
grass20 = Grasshopper(player2, (2,0))
grass11 = Grasshopper(player1, (1,-1))
grassn11 = Grasshopper(player1, (-1,1))
board.addPiece(grass1, 0, 0)
# board.addPiece(grass2, 1, 0)
# board.addPiece(grass3, 0, 1)
# board.addPiece(grass02, 0, 2)
# board.addPiece(grass20, 2, 0)
# board.addPiece(grass11, 1,-1)
board.addPiece(grassn11, -1, 1)
print(grass1.getMoves(board))