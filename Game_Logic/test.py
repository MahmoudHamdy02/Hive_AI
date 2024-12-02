import sys
import os

# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Game_Logic.Game.GameController import GameController

# board=Board()
# white_player=Player(Color.WHITE)
# black_player=Player(Color.BLACK)
# game=GameStatus(board,white_player,black_player)
# controller=GameController(board)
# ant=Ant()
# bee=Bee()
# spider=Spider()
# grasshopper=Grasshopper()
# beetle=Beetle()

# while not game.check_victory:
#   controller.add_piece(game,board,'ant',(0,0),white_player)
#   controller.add_piece(game,board,'ant',(0,1),black_player)
  # controller.add_piece(game,board,'ant',(0,0),white_player)
  # controller.add_piece(game,board,'ant',(0,0),white_player)

controller = GameController()
# PLayer1
# print(controller.get_valid_adds())
controller.add_piece('ant', (0, 0))
# PLayer2

# print(controller.get_valid_adds())
controller.add_piece('ant', (0, 1))
# PLayer1
# print(controller.get_valid_adds())
controller.add_piece('ant', (0, -1))
# # PLayer2
controller.add_piece('grasshopper', (0, 2))

controller.add_piece('ant', (0, -2))

#PLayer2
print(controller.get_valid_moves((0, 2)))
# controller.move_piece((0, 2), (1, -1))


# # PLayer1
# print("Turn 4")
# print(controller.get_valid_adds())
# controller.add_piece('ant', (0, 4))




