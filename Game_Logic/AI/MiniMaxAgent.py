from Game_Logic.AI.Agent import Agent

class MiniMaxAgent(Agent):
    """AI agent that uses the minimax algorithm to make decisions"""
    
    def __init__(self, gameController, agentColor):
        super().__init__(gameController, agentColor)
        
    def getBestMove(self, maxDepth: int, timeLimit: float) -> tuple:
        pass