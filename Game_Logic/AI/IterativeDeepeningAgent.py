from Game_Logic.AI.Agent import Agent
import time
import copy

class IterativeDeepeningAgent(Agent):
    """AI agent that uses the iterative deepening algorithm with alpha-beta pruning."""

    def __init__(self, originalGameController, agentColor, maxDepth, timeLimit):
        super().__init__(originalGameController, agentColor, maxDepth, timeLimit)
        # self.bestMove = None  # Stores the best move across all iterations

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

        # Start with a deepcopy of the original game controller
        # gameControllerCopy = copy.deepcopy(self.originalGameController)
        # moves = gameControllerCopy.get_all_moves_and_adds()
        moves = self.originalGameController.get_all_moves_and_adds()

        for move in moves:
            if time.time() - start_time >= self.timeLimit:
                raise TimeoutError("Time limit exceeded during alpha-beta search")

            if not self.doMove(self.originalGameController, move):  
                continue

            value = self._alphaBeta(self.originalGameController, depth - 1, alpha, beta, False)
            self.undoMove( move)

            if value > bestValue:
                bestValue = value
                bestMove = move

            alpha = max(alpha, bestValue)
            if alpha >= beta:
                break

        return bestMove, bestValue


        # for move in moves:
        #     if time.time() - start_time >= self.timeLimit:
        #         raise TimeoutError("Time limit exceeded during alpha-beta search")

        #     # Create a new copy for each move
        #     GC_copy = copy.deepcopy(gameControllerCopy)
        #     if not self.doMove(GC_copy, move):  
        #         continue

        #     value = self._alphaBeta(GC_copy, depth - 1, alpha, beta, False, start_time)

        #     if value > bestValue:
        #         bestValue = value
        #         bestMove = move

        #     alpha = max(alpha, bestValue)
        #     if alpha >= beta:
        #         break

        # return bestMove, bestValue

    def _alphaBeta(self, gameController, depth: int, alpha: float, beta: float, maximizingPlayer: bool, start_time: float) -> float:
        """
        Recursive alpha-beta pruning function.
        """
        if time.time() - start_time >= self.timeLimit:
            raise TimeoutError("Time limit exceeded during alpha-beta search")

        moves = gameController.get_all_moves_and_adds()
        if depth <= 0 or len(moves) == 0:
            return self.heuristic.calculateBoardScore(gameController)

        # if maximizingPlayer:

        #     for move in moves:
        #         # Create a new copy for each recursive call
        #         GC_copy = copy.deepcopy(gameController)
        #         if not self.doMove(GC_copy, move):  
        #             continue

        #         value = self._alphaBeta(GC_copy, depth - 1, alpha, beta, False, start_time)

        #         alpha = max(alpha, value)
        #         if alpha >= beta:
        #             break

        #     return alpha
        if maximizingPlayer:
            maxValue = float('-inf')
            for move in moves:
                if time.time() - start_time >= self.timeLimit:
                    raise TimeoutError("Time limit exceeded during alpha-beta search")

                # Apply the move instead of deepcopy
                if not self.doMove(gameController, move):  
                    continue

                value = self._alphaBeta(gameController, depth - 1, alpha, beta, False, start_time)
                self.undoMove(move)  # Undo the move

                maxValue = max(maxValue, value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return maxValue

        # else:
        #     for move in moves:
              
        #         GC_copy = copy.deepcopy(gameController)
        #         if not self.doMove(GC_copy, move):  
        #             continue

        #         value = self._alphaBeta(GC_copy, depth - 1, alpha, beta, True, start_time)

        #         beta = min(beta, value)
        #         if alpha >= beta:
        #             break

        #     return beta

        else:
            minValue = float('inf')
            for move in moves:
                if time.time() - start_time >= self.timeLimit:
                    raise TimeoutError("Time limit exceeded during alpha-beta search")

                # Apply the move instead of deepcopy
                if not self.doMove(gameController, move):  
                    continue

                value = self._alphaBeta(gameController, depth - 1, alpha, beta, True, start_time)
                self.undoMove(move)  # Undo the move

                minValue = min(minValue, value)
                beta = min(beta, value)
                if alpha >= beta:
                    break

            return minValue
