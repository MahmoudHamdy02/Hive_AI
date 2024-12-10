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
controller.add_piece('bee', (0, 0))
# PLayer2

# # print(controller.get_valid_adds())
controller.add_piece('bee', (0, 1))
# # PLayer1
# # print(controller.get_valid_adds())
# controller.add_piece('ant', (0, -1))
# # # PLayer2
# controller.add_piece('grasshopper', (0, 2))

# controller.add_piece('ant', (0, -2))
m=152
print(str(m))
# #PLayer2
board=controller.get_board()

# controller.add_piece('spider', (-1,0))
# print (controller.get_valid_adds('spider'))
# controller.add_piece('spider', (0,2))
# print (controller.get_valid_adds('ant'))
# controller.add_piece('ant', (-1,-1))
# print (controller.get_valid_moves((-1,-1)))
# controller.add_piece('ant', (1, 1))
print(controller.get_all_possible_moves(board))
#controller.move_piece((0, 2), (0,-3))


# # PLayer1
# print("Turn 4")
# print(controller.get_valid_adds())


# print(controller.hasPlay())