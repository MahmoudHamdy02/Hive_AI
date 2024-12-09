from Game_Logic.Piece import Bee
from Game_Logic.Player.Color import Color
from Game_Logic.Game.GameController import GameController

class Heuristic:
    """ 
    Class that holds the heuristic functions for AI agents
    ref: https://liacs.leidenuniv.nl/~plaata1/papers/IEEE_Conference_Hive_D__Kampert.pdf

    """
    
    def __init__(self, gameController: GameController, agentColor: Color):
        self.gemeController = gameController
        self.agentColor = agentColor
        
        self.weights = {
            'win': 1e6,
            'loss': -1e6,
            'queen_surroundings': 10,
            'on_board_pieces': 1,
            'blocked_pieces': 5,
        }
        
        self.piece_values = {
            'Bee': 5,
            'Ant': 3,
            'Beetle': 1,
            'Grasshopper': 1,
            'Spider': 1
        }

    def calculateBoardScore(self) -> int:
        """ 
        Calculate the score of the board based on the following metrics:
        1. win and loss evaluation
        2. queen safety
        3. number of pieces on board
        5. blocked pieces on the board

        """

        # if the last move was a winning move for the current agent then return the maximum score
        winner = self.gemeController.get_winner()
        if winner:
            if (winner == 1 and self.agentColor == Color.WHITE) or (winner == 2 and self.agentColor == Color.BLACK):
                return self.weights['win']
            else:
                return self.weights['loss']

        # the last move was not a winning or losing move, so we calculate the score based on the other metrices
        score = self._calculate_queen_surroundings() + self._calculate_on_board_pieces() + self._calculate_blocked_pieces()
        return score

    def _calculate_queen_surroundings(self):
        """
        Calculate the score based on the number of surrounding pieces of the queen
        
        """

        grid = self.gemeController.get_board().getGrid()
        own_queen_neighbors = 0
        opponent_queen_neighbors = 0

        for position, cell in grid.items():
            current_piece = cell.getPiece()

            if current_piece is None:
                continue

            if isinstance(current_piece, Bee):
                neighbors_count = len(self.gemeController.board.getNeighbors(position))

                if current_piece.getOwner().get_color() == self.agentColor:
                    own_queen_neighbors += neighbors_count
                else:
                    opponent_queen_neighbors += neighbors_count

        return self.weights['queen_surroundings'] * (opponent_queen_neighbors - own_queen_neighbors)


    def _calculate_on_board_pieces(self):
        """ 
        Calculate the score based on the number of onboard pieces of the agent

        """

        grid = self.gemeController.get_board().getGrid()
        num_on_board_pieces = 0

        for cell in grid.values():
            pieces = cell.getPiecesList()
            
            for piece in pieces:
                if piece.getOwner().get_color() == self.agentColor:
                    num_on_board_pieces += 1 
        
        return self.weights['on_board_pieces'] * num_on_board_pieces
    
    def _calculate_blocked_pieces(self):
        """ 
        Calculate the score based on the number of blocked pieces on the board

        """

        grid = self.gemeController.get_board().getGrid()
        own_blocked_score = 0
        opponent_blocked_score = 0

        for position, cell in grid.items():
            current_piece = cell.getPiece()

            if current_piece is None:
                continue

            piece_value = self.piece_values[current_piece.__class__.__name__]
            valid_moves = self.gemeController.get_valid_moves(position)

            if len(valid_moves) == 0:
                if current_piece.getOwner().get_color() == self.agentColor:
                    own_blocked_score += piece_value
                else:
                    opponent_blocked_score += piece_value
                    
        return self.weights['blocked_pieces'] * (opponent_blocked_score - own_blocked_score)

