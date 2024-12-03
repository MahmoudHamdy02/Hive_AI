import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Game_Logic.Game.GameController import *
from Game_Logic.Piece import *

def Minimax():
    


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

