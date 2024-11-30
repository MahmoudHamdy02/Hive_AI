import sys
import os

# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Game_Logic.Board.Board import Board
from Game_Logic.Player.Player import Player
from Game_Logic.Piece.Bee import Bee
from Game_Logic.Piece.Ant import Ant
from Game_Logic.Player.Color import Color
from Game_Logic.Game.GameStatus import GameStatus

board = Board()
player1 = Player(Color.WHITE)
player2 = Player(Color.BLACK)

stat = GameStatus(board, player1, player2)

bee = Bee(player1)
ant = Ant(player2)
ant2 = Ant(player2)
ant3 = Ant(player2)
ant4 = Ant(player1)
ant5 = Ant(player1)
ant6 = Ant(player1)

board.addPiece(bee, 0, 0)
board.addPiece(ant, 1, 0)
board.addPiece(ant2, 0, 1)
board.addPiece(ant3, 1, -1)
board.addPiece(ant4, 0, -1)
board.addPiece(ant5, -1, 0)
board.addPiece(ant6, -1, 1)

print(stat.getCurrentPlayer().get_color())
print(stat.check_victory())
# Expected: False

stat.nextTurn()
print(stat.getCurrentPlayer().get_color())
print(stat.check_victory())
# Expected: True

stat.nextTurn()
print(stat.getCurrentPlayer().get_color())
print(stat.check_victory())