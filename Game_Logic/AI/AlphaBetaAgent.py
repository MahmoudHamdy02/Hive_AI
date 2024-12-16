from copy import deepcopy
from  Game_Logic.AI.Agent import Agent
from Game_Logic.Game.GameController import GameController

class AlphaBetaAgent(Agent):
    """AI agent that uses the alpha-beta pruning algorithm to make decisions"""
    
    def __init__(self, gameController, agentColor, maxDepth, timeLimit):
        super().__init__(gameController, agentColor, maxDepth, timeLimit)
        
    # def getBestMove(self) -> list | None:
    #     """ 
    #     Returns the best move for the agent using the alpha-beta pruning algorithm
    #     """
    #     bestMove = None
    #     bestValue = float('-inf')
    #     alpha = float('-inf')
    #     beta = float('inf')
    #     moves = self.gameController.get_all_moves_and_adds()
    #     self.move_history.clear()  
    #     for move in moves:
    #         if not self.doMove(move):  
    #             continue  
    #         value = self._alphaBeta(self.maxDepth - 1, alpha, beta, False)
    #         self.undoMove()

    #         if value > bestValue:
    #             bestValue = value
    #             bestMove = move

    #     return bestMove
    
    # def _alphaBeta(self, depth: int, alpha: float, beta: float, maximizingPlayer: bool) -> float:
    #     """
    #     Returns the best value that maximizer can obtain
    #     """
    #     moves = self.gameController.get_all_moves_and_adds()
    #     if depth <= 0 or len(moves) == 0:
    #         return self.heuristic.calculateBoardScore()
    
    #     if maximizingPlayer:
    #         for move in moves:
    #             if not self.doMove(move):  
    #                 continue  
    #             value = self._alphaBeta(depth - 1, alpha, beta, False)
    #             self.undoMove()

    #             alpha = max(alpha, value)
    #             if alpha >= beta:
    #                 break

    #         return alpha
        
    #     else:
    #         for move in moves:
    #             if not self.doMove(move):  
    #                 continue
    #             value = self._alphaBeta(depth - 1, alpha, beta, True)
    #             self.undoMove()

    #             beta = min(beta, value)
    #             if alpha >= beta:
    #                 break

    #         return beta
        
    def getBestMove(self) -> list | None:
        """ 
        Returns the best move for the agent using the alpha-beta pruning algorithm
        """
        bestMove = None
        bestValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

         # Start with a deep copy of the original game controller
        gameControllerCopy = deepcopy(self.originalGameController)
        moves = gameControllerCopy.get_all_moves_and_adds()
  
        for move in moves:
            GC_copy = deepcopy(gameControllerCopy)
            if not self.doMove(GC_copy, move):  
                continue  
            value = self._alphaBeta(GC_copy, self.maxDepth - 1, alpha, beta, False)

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
                GC_copy = deepcopy(gameController)
                if not self.doMove(GC_copy, move):  
                    continue  
                value = self._alphaBeta(GC_copy, depth - 1, alpha, beta, False)

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return alpha
        
        else:
            for move in moves:
                GC_copy = deepcopy(gameController)
                if not self.doMove(GC_copy, move):  
                    continue
                value = self._alphaBeta(GC_copy, depth - 1, alpha, beta, True)

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return beta