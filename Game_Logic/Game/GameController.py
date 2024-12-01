from Game_Logic.Board.Board import Board
from Game_Logic.Game.MoveFilter import MoveFilter
from Game_Logic.Piece.GrassHopper import Grasshopper
from Game_Logic.Piece.Ant import Ant
from Game_Logic.Piece.Bee import Bee
from Game_Logic.Piece.Spider import Spider

class GameController:
    def _init_(self, board):
        """
        Initializes the game controller with a game board.
        """
        self.board = board

    def get_valid_moves(self, piece, position):
        """
        Gets valid moves for a specific piece at a given position.
        Delegates move generation to the piece class and validation to MoveFilter.
        """
        piece_classes = {
            'Grasshopper': Grasshopper,
            'Ant': Ant,
            'Bee': Bee,
            'Spider': Spider
        }

        if piece not in piece_classes:
            raise ValueError(f"Unknown piece type: {piece}")

        # Get the potential moves from the piece class
        potential_moves = piece_classes[piece].get_moves(self.board, position)

        # Filter the moves using the MoveFilter class
        return MoveFilter.filter_moves(self.board, potential_moves,position)
    
        

