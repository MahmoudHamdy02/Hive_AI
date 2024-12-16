from Game_Logic.AI.Agent import Agent
from copy import deepcopy
from Game_Logic.Game.GameController import GameController
class MiniMaxAgent(Agent):
    """AI agent that uses the minimax algorithm to make decisions"""
    
    def __init__(self, gameController, agentColor, maxDepth,timeLimit):
        super().__init__(gameController, agentColor,maxDepth,timeLimit)

    def getBestMove(self) -> list | None:
        """
        Returns the best move for the agent using the alpha-beta pruning algorithm
        """
        bestMove = None
        bestValue = float('-inf')



        # Start with a deep copy of the original game controller
        gameControllerCopy = deepcopy(self.originalGameController)
        moves = gameControllerCopy.get_all_moves_and_adds()

        for move in moves:
            GC_copy = deepcopy(gameControllerCopy)
            if not self.doMove(GC_copy, move):
                continue
            value = self.minimax(GC_copy, self.maxDepth - 1,False)

            if value > bestValue:
                bestValue = value
                bestMove = move

        return bestMove

    def minimax(self, gameController: GameController, depth: int,maximizingPlayer: bool) -> float:
        """
        Returns the best value that maximizer can obtain
        """
        maxvalue=float('-inf')
        minvalue=float('inf')
        moves = gameController.get_all_moves_and_adds()
        if depth <= 0 or len(moves) == 0:
            return self.heuristic.calculateBoardScore(gameController)

        if maximizingPlayer:
            for move in moves:
                GC_copy = deepcopy(gameController)
                if not self.doMove(GC_copy, move):
                    continue
                value = self.minimax(GC_copy, depth - 1, False)

                maxvalue = max(maxvalue, value)


            return maxvalue

        else:
            for move in moves:
                GC_copy = deepcopy(gameController)
                if not self.doMove(GC_copy, move):
                    continue
                value = self.minimax(GC_copy, depth - 1, True)

                minvalue = min(minvalue, value)


            return minvalue