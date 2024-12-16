from Game_Logic.AI.IterativeDeepeningAgent import IterativeDeepeningAgent
from Game_Logic.Game.GameController import GameController
from Game_Logic.Player.Player import Player
from Game_Logic.Player.Color import Color

controller = GameController()

controller.add_piece('ant', (0, 0))

controller.add_piece('ant', (0, 1))
controller.add_piece('bee', (0,-1 ))
controller.add_piece('bee', (0, 2))
controller.add_piece('ant', (1,-1))
controller.get_valid_moves((0,0))

board=controller.get_board()

agent = IterativeDeepeningAgent(controller, Color.WHITE,10,3)

moves = agent.getBestMove()