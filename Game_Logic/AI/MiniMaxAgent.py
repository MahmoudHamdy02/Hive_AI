from Game_Logic.AI.Agent import Agent

class MiniMaxAgent(Agent):
    """AI agent that uses the minimax algorithm to make decisions"""
    
    def __init__(self, gameController, agentColor,maxDepth, timeLimit):
        super().__init__(gameController, agentColor,maxDepth, timeLimit)
        
    def getBestMove(self) -> tuple:
        """
        Returns the best move for the agent using the minimax pruning algorithm
        """
        bestMove = None
        bestValue = float('-inf')
        moves = self.gameController.get_all_moves_and_adds()
        self.move_history.clear()

        for move in moves:
            if not self.doMove(move):
                continue
            value = self.minimax(self.maxDepth - 1,False)
            self.undoMove()

            if value > bestValue:
                bestValue = value
                bestMove = move

        return bestMove

    def minimax(self, depth: int, maximizingPlayer: bool) -> float:
        """
        Returns the best value that maximizer can obtain
        """
        bestValuemax = float('-inf')
        bestValuemin = float('inf')
        moves = self.gameController.get_all_moves_and_adds()

        if depth <= 0 or len(moves) == 0:
            return self.heuristic.calculateBoardScore()

        if maximizingPlayer:
            for move in moves:
                if not self.doMove(move):
                    continue
                value = self.minimax(depth - 1,False)
                self.undoMove()

                bestValuemax = max(bestValuemax, value)
                print(bestValuemax)



            return bestValuemax

        else:
            for move in moves:
                if not self.doMove(move):
                    continue
                value = self.minimax(depth - 1,True)
                self.undoMove()

                bestValuemin = min(bestValuemin, value)
                print(bestValuemin)
            return bestValuemin