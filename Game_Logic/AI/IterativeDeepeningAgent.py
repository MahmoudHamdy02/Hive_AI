from Game_Logic.AI.Agent import Agent
import time

class IterativeDeepeningAgent(Agent):
    """AI agent that uses the iterative deepening algorithm to make decisions"""
    
    def __init__(self, gameController, agentColor, maxDepth, timeLimit):
        super().__init__(gameController, agentColor, maxDepth, timeLimit)
        self.bestMove = None  # Stores the best move across all iterations

    def getBestMove(self) -> list | None:
        """ 
        Returns the best move for the agent using the alpha-beta pruning algorithm 
        with iterative deepening.
        """
        self.bestMove = None
        start_time = time.time()
        depth = 1

        while depth <= self.maxDepth:
            elapsed_time = time.time() - start_time
            if elapsed_time >= self.timeLimit:
                break

            try:
                bestMove, bestValue = self._alphaBetaIterative(depth, start_time)
                self.bestMove = bestMove
            except TimeoutError:
                break

            depth += 1

        return self.bestMove

    def _alphaBetaIterative(self, depth: int, start_time: float) -> tuple:
        """
        Perform alpha-beta pruning for a given depth and track the best move.
        """
        bestMove = None
        bestValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        moves = self.gameController.get_all_moves_and_adds()
        self.move_history.clear()

        for move in moves:
            if time.time() - start_time >= self.timeLimit:
                raise TimeoutError("Time limit exceeded during alpha-beta search")

            if not self.doMove(move):  
                continue  
            value = self._alphaBeta(depth - 1, alpha, beta, False, start_time)
            self.undoMove()

            if value > bestValue:
                bestValue = value
                bestMove = move

            alpha = max(alpha, bestValue)
            if alpha >= beta:
                break

        return bestMove, bestValue

    def _alphaBeta(self, depth: int, alpha: float, beta: float, maximizingPlayer: bool, start_time: float) -> float:
        """
        Recursive alpha-beta pruning function.
        """
        if time.time() - start_time >= self.timeLimit:
            raise TimeoutError("Time limit exceeded during alpha-beta search")

        moves = self.gameController.get_all_moves_and_adds()

        if depth <= 0 or len(moves) == 0:
            return self.heuristic.calculateBoardScore()
        
        if maximizingPlayer:
            for move in moves:
                if not self.doMove(move):  
                    continue  
                value = self._alphaBeta(depth - 1, alpha, beta, False, start_time)
                self.undoMove()

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return alpha
        else:
            for move in moves:
                if not self.doMove(move):  
                    continue  
                value = self._alphaBeta(depth - 1, alpha, beta, True, start_time)
                self.undoMove()

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return beta