from abc import ABC, abstractmethod
from Game_Logic.AI.Heuristic import Heuristic
from Game_Logic.Player.Color import Color
from Game_Logic.Game.GameController import GameController
from copy import deepcopy

class Agent(ABC):
    """Abstract parent class for AI agents"""

    def __init__(self,  originalGameController: GameController, agentColor: Color, maxDepth: int, timeLimit: float):
        # self.gameController = gameController
        self.originalGameController = originalGameController
        self.agentColor = agentColor
        self.maxDepth = maxDepth
        self.timeLimit = timeLimit
        # self.heuristic = Heuristic(gameController, agentColor)
        self.heuristic = Heuristic(agentColor)
        # self.move_history = []

    @abstractmethod
    def getBestMove(self) -> list | None:
        """
        Returns the best move for the agent,
        A move is a list of the form [pieceType, old_position(tuble), new_position(tuble)]
        """
        pass

    def doMove(self, gameController: GameController, move: list):
        """Applies a move to the provided game controller"""
        piece_type, old_pos, new_pos = move

        if old_pos is None:
            return gameController.add_piece(piece_type, new_pos)
        else:
            return gameController.move_piece(old_pos, new_pos)

    def undoMove(self, move):
        piece_type, old_pos, new_pos = move
        if old_pos is None:
            self.originalGameController.undoAdd(piece_type,new_pos)
        else:
            self.originalGameController.undoMove(new_pos, old_pos)


