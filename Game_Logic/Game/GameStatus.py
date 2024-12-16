from Game_Logic.Piece import Bee
from Game_Logic.Player.Color import Color
class GameStatus:
    def __init__(self, board, whitePlayer, blackPlayer):
        self.board = board
        self.turn_count = 0
        self.players = [whitePlayer, blackPlayer]
        self.current_player = whitePlayer
        self.winner = None
    
    def nextTurn(self):
        self.turn_count += 1
        self.current_player = self.players[self.turn_count % 2]
    
    def getCurrentPlayer(self):
        return self.current_player
    
    def check_defeat(self) -> int:
        """
        Check if the opponent's Queen Bee is surrounded and thus the game is over.
        return: True if the opponent's Queen Bee is surrounded, False otherwise.
        """
        for (q, r) in self.board.getGrid().keys():
            if not self.board.hasPieceAt(q, r):
                continue

            piece = self.board.getPieceAt(q, r)
            # If board has a queen bee at q, r and it is the opponent's queen bee
            if (isinstance(piece, Bee)):
                # Check if the opponent's Queen Bee is surrounded
                if len(self.board.getNeighbors((q, r))) == 6:
                    if piece.getOwner().color == Color.BLACK:
                        return 2
                    elif piece.getOwner().color == Color.WHITE:
                        return 1
                    
        return False
    
    def getTurnNumber(self):
        return self.turn_count

    def setCurrentPlayer(self, player):
        self.current_player = player
    
    def setTurnNumber(self, turn):
        self.turn_count = turn