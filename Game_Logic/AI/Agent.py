from abc import ABC, abstractmethod
from Game_Logic.AI.Heuristic import Heuristic
from Game_Logic.Player.Color import Color
from Game_Logic.Game.GameController import GameController

class Agent(ABC):
    """Abstract parent class for AI agents"""

    def __init__(self,  gameController: GameController, agentColor: Color, maxDepth: int, timeLimit: float):
        self.gameController = gameController
        self.agentColor = agentColor
        self.maxDepth = maxDepth
        self.timeLimit = timeLimit
        self.heuristic = Heuristic(gameController, agentColor)
        self.move_history = []

    @abstractmethod
    def getBestMove(self) -> list | None:
        """
        Returns the best move for the agent,
        A move is a list of the form [pieceType, old_position(tuble), new_position(tuble)]
        """
        pass

    def doMove(self, move: list):
        """Applies a move to the game board"""
        current_state = {
            'move': move,
            'player': self.gameController.get_status().getCurrentPlayer(),
            'turn': self.gameController.get_status().getTurnNumber(),
            'grid': self.gameController.get_board().getGrid().copy(),
            'pieces': {
                'white': self.gameController.white_player.get_remaining_pieces().copy(),
                'black': self.gameController.black_player.get_remaining_pieces().copy()
            }
        }
        
        piece_type, old_pos, new_pos = move

        success = False
        if old_pos is None:
            success = self.gameController.add_piece(piece_type, new_pos)
        else:
            success = self.gameController.move_piece(old_pos, new_pos)
            
        if success:
            self.move_history.append(current_state)

        return success

    def undoMove(self):
        """Restore game state before last move"""
        if not self.move_history:
            return False
            
        state = self.move_history.pop()
        self.gameController.restore_state(state)
        return True
            
        


