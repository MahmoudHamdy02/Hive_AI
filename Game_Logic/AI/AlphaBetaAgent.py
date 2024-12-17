import random
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
            value = self._alphaBeta(self.maxDepth - 1, alpha, beta, False)
            self.undoMove(move)
            if value == float('inf'):
                return move

            if value > bestValue:
                bestValue = value
                bestMove = move

        return bestMove
    
    def _alphaBeta(self, depth: int, alpha: float, beta: float, maximizingPlayer: bool) -> float:
        """
        Returns the best value that maximizer can obtain
        """
        len_moves = 0
        move_scores = []
        moves = self.originalGameController.get_all_moves_and_adds()
        # moves = self.order_moves(moves)
        # moves = moves[:10]
        if len(moves) > 10:
            moves = random.sample(moves, 10)
        if depth <= 0 or len(moves) == 0:
            return self.heuristic.calculateBoardScore(self.originalGameController)
    
        if maximizingPlayer:
            maxValue = float('-inf')
            for move in moves:
                len_moves += 1
                if not self.doMove(self.originalGameController, move):  
                    continue
                value = self._alphaBeta(depth - 1, alpha, beta, False)
                self.undoMove(move)
                if value == float('inf'):
                    return value

                maxValue = max(maxValue, value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    # print(alpha, beta)
                    # print("pruning")
                    print("pruned",len_moves)
                    return maxValue
            print("not pruned",len_moves)
            return maxValue
        
        else:
            minValue = float('inf')
            for move in moves:
                len_moves += 1
                if not self.doMove(self.originalGameController, move):  
                    continue
                value = self._alphaBeta(depth - 1, alpha, beta, True)
                self.undoMove(move)
                if value == float('-inf'):
                    return value

                minValue = min(minValue, value)
                beta = min(beta, value)
                if alpha >= beta:
                    # print(alpha, beta)
                    # print("pruning")
                    print("pruned",len_moves)
                    return minValue
            
            # print(alpha, beta)
            print("not pruned",len_moves)
            return minValue
        
    def order_moves(self, moves: list) -> list:
        """ 
        Orders the moves based on the heuristic value of the game state after each move
        """
        move_values = []
        for move in moves:
            self.doMove(self.originalGameController,move)
            move_value = self.heuristic.calculateBoardScore(self.originalGameController)
            self.undoMove(move)
            move_values.append((move_value, move))
        
        # Sort moves based on the heuristic values in descending order
        move_values.sort(reverse=True, key=lambda x: x[0])
        
        # Extract the sorted moves
        sorted_moves = [move for _, move in move_values]
        values = [value for value, _ in move_values]
        print(values[:10])
        
        return sorted_moves