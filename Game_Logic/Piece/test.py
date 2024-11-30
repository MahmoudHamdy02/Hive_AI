
from Game_Logic.Board.Board import Board
from Game_Logic.Player.Player import Player,Color
from Game_Logic.Piece.Spider import Spider
board = Board()
player1 = Player(Color.WHITE)
player2 = Player(Color.BLACK)
grass1 = Spider(player1, (0, -1))
grass2 = Spider(player2, (1, -1))
grass3 = Spider(player1, (1, 0))
grass02 = Spider(player2, (0, 1))
grass20 = Spider(player2, (-1, 1))
grass11 = Spider(player1, (-1, 0))
grassn_11 = Spider(player1, (0, 0))
board.addPiece(grass1, 0, -1)
#board.addPiece(grass2, 1, -1)
board.addPiece(grass3, 1, 0)
board.addPiece(grass02, 0, 1)
board.addPiece(grass20, -1, 1)
board.addPiece(grass11, -1, 0)
board.addPiece(grassn_11, 0,0)
print(grassn_11.getMoves(board))