from Game_Logic.AI.Agent import Agent
import time
import copy
import hashlib

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
        # self.lastMove = None
        start_time = time.time()
        depth = 1

        while depth <= self.maxDepth:
            elapsed_time = time.time() - start_time
            if elapsed_time >= self.timeLimit:
                break

            try:
                bestMove, bestValue = self._alphaBetaIterative(depth, start_time)
                if bestValue == float('inf'):
                    return bestMove
                self.bestMove = bestMove
            except TimeoutError:
                print(f"Time limit exceeded for depth {depth}")
                break

            depth += 1

        return self.bestMove

    def _alphaBetaIterative(self, depth: int, start_time: float) -> tuple:
        """
        Perform alpha-beta pruning for a given depth and track the best move.
        """
        bestValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')


        moves = self.originalGameController.get_all_moves_and_adds()
  

        for move in moves:
            if time.time() - start_time >= self.timeLimit:
                raise TimeoutError("Time limit exceeded during alpha-beta search")

            if not self.doMove(self.originalGameController, move):  
                continue
            # self.lastMove = move
            self.originalGameController.status.prevTurn()
            winner = self.originalGameController.status.check_victory()
            if winner:
                print("winner MAX", winner)
                # if (winner == 1 and self.agentColor == 0) or (winner == 2 and self.agentColor == 1):
                print("I WIN", self.agentColor)
                return move, float('inf')
            self.originalGameController.status.nextTurn()
            value = self._alphaBeta(self.originalGameController, depth - 1, alpha, beta, False, start_time)
            if value == float('inf'):
                return move, value
            self.undoMove(move)

            if value > bestValue:
                bestValue = value
                self.bestMove = move

            alpha = max(alpha, bestValue)
            if alpha >= beta:
                break

        return self.bestMove, bestValue


    def _alphaBeta(self, gameController, depth: int, alpha: float, beta: float, maximizingPlayer: bool, start_time: float) -> float:
        """
        Recursive alpha-beta pruning function.
        """
        if time.time() - start_time >= self.timeLimit:
            # self.undoMove(self.lastMove)
            raise TimeoutError("Time limit exceeded during alpha-beta search")

        moves = gameController.get_all_moves_and_adds()
        if depth <= 0 or len(moves) == 0:
            return self.heuristic.calculateBoardScore(gameController)

        # # Move ordering: Sort moves based on heuristic scores
        # moves.sort(key=lambda move: self.heuristic.evaluateMove(gameController, move), reverse=maximizingPlayer)

        if maximizingPlayer:
            maxValue = float('-inf')
            for move in moves:
                if time.time() - start_time >= self.timeLimit:
                    # self.undoMove(self.lastMove)
                    raise TimeoutError("Time limit exceeded during alpha-beta search")

                # Apply the move instead of deepcopy
                if not self.doMove(gameController, move):  
                    continue
                # self.lastMove = move
                # self.originalGameController.status.prevTurn()
                # winner = self.originalGameController.status.check_victory()
                # if winner:
                #     print("winner MAX", winner)
                #     # if (winner == 1 and self.agentColor == 0) or (winner == 2 and self.agentColor == 1):
                #     print("I WIN", self.agentColor)
                #     return float('inf')
                # self.originalGameController.status.nextTurn()
                print(self.originalGameController.status.getCurrentPlayer().get_color())
                value = self._alphaBeta(gameController, depth - 1, alpha, beta, False, start_time)
                self.undoMove(move)  # Undo the move
                if value == float('inf'):
                    return value
                maxValue = max(maxValue, value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            print("max",maxValue)
            return maxValue
        else:
            minValue = float('inf')
            for move in moves:
                if time.time() - start_time >= self.timeLimit:
                    # self.undoMove(self.lastMove)
                    raise TimeoutError("Time limit exceeded during alpha-beta search")

                if not self.doMove(gameController, move):  
                    continue
                # self.lastMove = move
                print(self.originalGameController.status.getCurrentPlayer().get_color())
                value = self._alphaBeta(gameController, depth - 1, alpha, beta, True, start_time)
                self.undoMove(move)  # Undo the move

                minValue = min(minValue, value)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            print("min",minValue)
            return minValue




# class IterativeDeepeningAgent(Agent):
#     """AI agent that uses the iterative deepening algorithm with alpha-beta pruning."""
    
#     def __init__(self, originalGameController, agentColor, maxDepth, timeLimit):
#         super().__init__(originalGameController, agentColor, maxDepth, timeLimit)
#         self.bestMove = None
#         self.previousBestMove = None  # To store the best move for move ordering
#         self.transposition_table = {}  # Hash-based transposition table for caching

#     def getBestMove(self) -> list | None:
#         """
#         Returns the best move for the agent using the alpha-beta pruning algorithm
#         with iterative deepening.
#         """
#         self.bestMove = None
#         start_time = time.time()
#         depth = 1

#         while depth <= self.maxDepth:
#             elapsed_time = time.time() - start_time
#             if elapsed_time >= self.timeLimit:
#                 break

#             try:
#                 bestMove, bestValue = self._alphaBetaIterative(depth, start_time)
#                 if bestMove:  # Update best move for move ordering
#                     self.previousBestMove = bestMove
#                     self.bestMove = bestMove
#             except TimeoutError:
#                 print(f"Time limit exceeded for depth {depth}")
#                 break

#             depth += 1

#         return self.bestMove

#     def _alphaBetaIterative(self, depth: int, start_time: float) -> tuple:
#         """
#         Perform alpha-beta pruning for a given depth and track the best move.
#         """
#         bestMove = None
#         bestValue = float('-inf')
#         alpha = float('-inf')
#         beta = float('inf')

#         moves = self.originalGameController.get_all_moves_and_adds()

#         # Move Ordering Optimization: Prioritize the best move from the previous depth
#         if self.previousBestMove and self.previousBestMove in moves:
#             moves.remove(self.previousBestMove)
#             moves.insert(0, self.previousBestMove)

#         for move in moves:
#             if time.time() - start_time >= self.timeLimit:
#                 raise TimeoutError("Time limit exceeded during alpha-beta search")

#             if not self.doMove(self.originalGameController, move):  
#                 continue

#             value = self._alphaBeta(self.originalGameController, depth - 1, alpha, beta, False, start_time)
#             self.undoMove(move)

#             if value > bestValue:
#                 bestValue = value
#                 bestMove = move

#             alpha = max(alpha, bestValue)
#             if alpha >= beta:
#                 break

#         return bestMove, bestValue

#     def _alphaBeta(self, gameController, depth: int, alpha: float, beta: float, maximizingPlayer: bool, start_time: float) -> float:
#         """
#         Recursive alpha-beta pruning function with transposition table and move ordering.
#         """
#         # Check for timeout
#         if time.time() - start_time >= self.timeLimit:
#             raise TimeoutError("Time limit exceeded during alpha-beta search")

#         # Generate a hash for the current board state
#         state_hash = self._generate_state_hash(gameController)

#         # Check transposition table for cached results
#         if (state_hash, depth) in self.transposition_table:
#             return self.transposition_table[(state_hash, depth)]

#         # Get all valid moves
#         moves = gameController.get_all_moves_and_adds()
#         if depth <= 0 or len(moves) == 0:
#             return self.heuristic.calculateBoardScore(gameController)

#         # Move Ordering: Sort moves based on heuristic evaluation
#         moves.sort(key=lambda move: self.heuristic.evaluateMove(gameController, move), reverse=maximizingPlayer)

#         if maximizingPlayer:
#             maxValue = float('-inf')
#             for move in moves:
#                 if time.time() - start_time >= self.timeLimit:
#                     raise TimeoutError("Time limit exceeded during alpha-beta search")

#                 if not self.doMove(gameController, move):  
#                     continue

#                 value = self._alphaBeta(gameController, depth - 1, alpha, beta, False, start_time)
#                 self.undoMove(move)

#                 maxValue = max(maxValue, value)
#                 alpha = max(alpha, value)
#                 if alpha >= beta:
#                     break

#             # Store result in transposition table
#             self.transposition_table[(state_hash, depth)] = maxValue
#             return maxValue
#         else:
#             minValue = float('inf')
#             for move in moves:
#                 if time.time() - start_time >= self.timeLimit:
#                     raise TimeoutError("Time limit exceeded during alpha-beta search")

#                 if not self.doMove(gameController, move):  
#                     continue

#                 value = self._alphaBeta(gameController, depth - 1, alpha, beta, True, start_time)
#                 self.undoMove(move)

#                 minValue = min(minValue, value)
#                 beta = min(beta, value)
#                 if alpha >= beta:
#                     break

#             # Store result in transposition table
#             self.transposition_table[(state_hash, depth)] = minValue
#             return minValue

#     def _generate_state_hash(self, gameController):
#         """
#         Generate a hash for the current game state using board positions.
#         """
#         board_state = str(gameController.board)  # Represent the board as a string
#         return hashlib.md5(board_state.encode()).hexdigest()
