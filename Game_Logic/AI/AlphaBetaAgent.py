from copy import deepcopy
from  Game_Logic.AI.Agent import Agent
from Game_Logic.Game.GameController import GameController

class AlphaBetaAgent(Agent):
    """AI agent that uses the alpha-beta pruning algorithm to make decisions"""
    
    def __init__(self, gameController, agentColor, maxDepth, timeLimit):
        super().__init__(gameController, agentColor, maxDepth, timeLimit)
        
        
    def getBestMove(self) -> list | None:
        """ 
        Returns the best move for the agent using the alpha-beta pruning algorithm
        """
        bestMove = None
        bestValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

         # Start with a deep copy of the original game controller
        # gameControllerCopy = deepcopy(self.originalGameController)
        
        moves = self.originalGameController.get_all_moves_and_adds()
  
        for move in moves:
            if not self.doMove(self.originalGameController, move):  
                continue  
            value = self._alphaBeta(self.originalGameController, self.maxDepth - 1, alpha, beta, False)
            self.undoMove(move)

            if value > bestValue:
                bestValue = value
                bestMove = move

        return bestMove
    
    def _alphaBeta(self, gameController: GameController, depth: int, alpha: float, beta: float, maximizingPlayer: bool) -> float:
        """
        Returns the best value that maximizer can obtain
        """
        moves = gameController.get_all_moves_and_adds()
        if depth <= 0 or len(moves) == 0:
            return self.heuristic.calculateBoardScore(gameController)
    
        if maximizingPlayer:
            for move in moves:
                if not self.doMove(self.originalGameController, move):  
                    continue  
                value = self._alphaBeta(self.originalGameController, depth - 1, alpha, beta, False)
                self.undoMove(move)

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return alpha
        
        else:
            for move in moves:
                if not self.doMove(self.originalGameController, move):  
                    continue
                value = self._alphaBeta(self.originalGameController, depth - 1, alpha, beta, True)
                self.undoMove(move)

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return beta