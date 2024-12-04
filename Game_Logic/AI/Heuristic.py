from Game_Logic.Player.Color import Color
from Game_Logic.Board.Board import Board

class Heuristic:
    """ Class that holds the heuristic functions for the AI agents"""
    
    def __init__(self, agentColor: Color, Board: Board):
        self.agentColor = agentColor
        self.board = Board
        self.weights = {}

    def calculateBoardScore(self) -> int:
        """Calculates the score of the board for the given player after making a move"""
        pass