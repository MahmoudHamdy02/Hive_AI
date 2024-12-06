from abc import ABC, abstractmethod

from Game_Logic.AI.Heuristic import Heuristic
from Game_Logic.Player.Color import Color
from Game_Logic.Board.Board import Board
from Game_Logic.Game.GameStatus import GameStatus
from Game_Logic.Game.GameController import GameController

class Agent(ABC):
    """Abstract parent class for AI agents"""

    def __init__(self,  gameController: GameController, agentColor: Color):
        self.agentColor = agentColor
        self.gameController = gameController
        self.heuristic = Heuristic(gameController, agentColor)

    @abstractmethod
    def getBestMove(self,  maxDepth: int, timeLimit: float) -> tuple:
        """
         gets all possible moves for the agentColor from the gameController,
         calculates the score of each move using the heuristic and
         return the move with the highest score
        """
        pass