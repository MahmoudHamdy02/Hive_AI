from  Game_Logic.AI.Agent import Agent

class AlphaBetaAgent(Agent):
    """AI agent that uses the alpha-beta pruning algorithm to make decisions"""
    
    def __init__(self, gameController, agentColor):
        super().__init__(gameController, agentColor)
        
    def getBestMove(self, maxDepth: int, timeLimit: float) -> tuple:
        pass