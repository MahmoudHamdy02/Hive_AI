from Game_Logic.Piece.Bee import Bee
from Game_Logic.Game.GameStatus import GameStatus
from Game_Logic.Game.GameController import GameController
from Game_Logic.Board.Board import Board
from Game_Logic.Game.MoveFilter import MoveFilter
from Game_Logic.Piece.GrassHopper import Grasshopper
from Game_Logic.Piece.Ant import Ant
from Game_Logic.Piece.Bee import Bee
from Game_Logic.Piece.Spider import Spider
from Game_Logic.Piece.Beetle import Beetle
from Game_Logic.Player.Player import Player
from Game_Logic.Player.Color import Color


board=Board()
white_player=Player(Color.WHITE)
black_player=Player(Color.BLACK)
game=GameStatus(board,white_player,black_player)
controller=GameController(board)
ant=Ant()
bee=Bee()
spider=Spider()
grasshopper=Grasshopper()
beetle=Beetle()

while not game.check_victory:
  controller.add_piece(game,board,'ant',(0,0),white_player)
  controller.add_piece(game,board,'ant',(0,1),black_player)
  # controller.add_piece(game,board,'ant',(0,0),white_player)
  # controller.add_piece(game,board,'ant',(0,0),white_player)



