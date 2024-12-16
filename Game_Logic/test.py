# import sys
# import os

# Add the root directory of the project to the sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
#
# from Game_Logic.Game.GameController import GameController
# from Game_Logic.AI.AlphaBetaAgent import AlphaBetaAgent
# from Game_Logic.Player.Color import Color
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

# controller = GameController()


# print("pieces before adding")
# pieces = controller.white_player.get_remaining_pieces()
# for piece_type, pieces in pieces.items():
#     print(f"{piece_type}: {len(pieces)}")

# # PLayer1
# # print(controller.get_valid_adds())
#controller.add_piece('ant', (-5,6))
# # PLayer2
#
# # # print(controller.get_valid_adds())
# # controller.add_piece('ant', (1, 0))
# # # PLayer1
# # # print(controller.get_valid_adds())
# # controller.add_piece('bee', (-1, 0))
# # # # PLayer2
# # controller.add_piece('bee', (2, 0))
#
# # controller.add_piece('ant', (0,-1))
#
# # controller.add_piece("beetle", (2, 1))
#
# # controller.move_piece((0, -1), (3,1))
#
#  controller.add_piece("ant", (1, 2))
# #
#  controller.add_piece("ant", (-1, -1))
# #
#  controller.add_piece("ant", (-1, 1))

# print("pieces after adding")
# pieces = controller.white_player.get_remaining_pieces()
# for piece_type, pieces in pieces.items():
#     print(f"{piece_type}: {len(pieces)}")

# controller.move_piece((1, -1), (-2, -2))
#
# controller.move_piece((1, -1), (0, -2))


# controller.add_piece('bee', (1,2))

#PLayer2
# print(controller.get_valid_moves((0, 2)))
# controller.move_piece((0, 2), (0,-3))

# print("state before agent")
# grid = controller.get_board().getGrid()
# for position, cell in grid.items():
#     print(f"{position}: {cell.getPiecesList()}")
#
# print(controller.get_status().getCurrentPlayer().get_color())
# print(controller.get_status().getTurnNumber())
# pieces = controller.white_player.get_remaining_pieces()
# for piece_type, pieces in pieces.items():
#     print(f"{piece_type}: {len(pieces)}")
#
# pieces = controller.black_player.get_remaining_pieces()
# for piece_type, pieces in pieces.items():
#     print(f"{piece_type}: {len(pieces)}")
#
# piece = controller.get_board().getPieceAt(0, 0)
# print(piece.getOwner())
# print(controller.white_player)
# print(controller.black_player)
# all_moves_and_adds = controller.get_all_moves_and_adds()
# print(all_moves_and_adds)

####
# agent1 = AlphaBetaAgent(controller, Color.WHITE, 3, 10)
# agent2 = AlphaBetaAgent(controller, Color.BLACK, 2, 10)
# move = agent1.getBestMove()
# print(move)
#####

# print("state after agent")
# grid = controller.get_board().getGrid()
# for position, cell in grid.items():
#     print(f"{position}: {cell.getPiecesList()}")
#
# print(controller.get_status().getCurrentPlayer().get_color())
# print(controller.get_status().getTurnNumber())
# pieces = controller.white_player.get_remaining_pieces()
# for piece_type, pieces in pieces.items():
#     print(f"{piece_type}: {len(pieces)}")
#
# pieces = controller.black_player.get_remaining_pieces()
# for piece_type, pieces in pieces.items():
#     print(f"{piece_type}: {len(pieces)}")
#
# piece = controller.get_board().getPieceAt(0, 0)
# print(piece.getOwner())
# print(controller.white_player)
# print(controller.black_player)
# all_moves_and_adds = controller.get_all_moves_and_adds()
# print(all_moves_and_adds)
#
#
# piece_type, old_pos, new_pos = move
# if old_pos is None:
#     controller.add_piece(piece_type, new_pos)
# else:
#     controller.move_piece(old_pos, new_pos)

# pieces = controller.black_player.get_remaining_pieces().copy()
#
# for piece_type, pieces in pieces.items():
#     print(f"{piece_type}: {len(pieces)}")
#
# pieces = controller.white_player.get_remaining_pieces().copy()
#
# for piece_type, pieces in pieces.items():
#     print(f"{piece_type}: {len(pieces)}")


# while not controller.get_winner():
#     current_player = controller.get_status().getCurrentPlayer().get_color()
#     remaining_pieces = controller.get_status().getCurrentPlayer().get_remaining_pieces()
#     for piece_type, pieces in remaining_pieces.items():
#         print(f"{piece_type}: {len(pieces)}")
#
#     if current_player == Color.WHITE:
#         move = agent1.getBestMove()
#         print(move)
#         if not move:
#             continue
#         piece_type, old_pos, new_pos = move
#
#         if old_pos is None:
#             controller.add_piece(piece_type, new_pos)
#         else:
#             controller.move_piece(old_pos, new_pos)
#     else:
#         move = agent2.getBestMove()
#         print(move)
#
#         if not move:
#             continue
#         piece_type, old_pos, new_pos = move
#         if old_pos is None:
#             controller.add_piece(piece_type, new_pos)
#         else:
#             controller.move_piece(old_pos, new_pos)
#
# print ("the winner is", controller.get_winner())
# # PLayer1
# print("Turn 4")
# print(controller.get_valid_adds())
# controller.add_piece('ant', (0, 4))

#print(controller.hasPlay())

import sys
import os
# Add the root directory of the project to the sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), '../')))

from Game_Logic.Game.GameController import GameController
from Game_Logic.AI.AlphaBetaAgent import AlphaBetaAgent
from Game_Logic.Player.Color import Color
import time

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
controller.add_piece('bee', (0, -1))
# # PLayer2
controller.add_piece('bee', (0, 2))

controller.add_piece('ant', (1, 1))

agent = AlphaBetaAgent(controller,Color.WHITE , 3, 1)
bestMove=agent.getBestMove()
print(bestMove)
# #PLayer2
# print(controller.get_valid_moves((0, 2)))
# controller.move_piece((0, 2), (0,-3))


# # # PLayer1
# # print("Turn 4")
# # print(controller.get_valid_adds())
# # controller.add_piece('ant', (0, 4))

# print(controller.hasPlay())

