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
        potential_moves =piece.get_moves(self.board, position)

        # Filter the moves using the MoveFilter class
        return MoveFilter.filter_moves(self.board, potential_moves,position)
    
    def move_piece(board, move,current_position,piece,current_player,self,status):
        if move in self.get_valid_moves(piece,current_position):
             board.grid.pop(current_position)  # Remove the piece from its current position
             board.grid[move] = piece
             current_player.remove_position(current_position)
             current_position.add_position(current_position)
             status.nextTurn()
        else:
             raise ValueError(f"Unknown piece type: {piece}")

    
    def add_piece(status,board, piece, target_position,current_player):
            q,r=target_position
            if (q,r) in board.grid:
                print(f"({q}, {r}) is already occupied!")
                return

            if piece not in status.pieces[status.current_player] or status.pieces[status.current_player][piece] <= 0:
                print(f"No more {piece}s available for {status.current_player}.")
                return
            # Needed to be checked 
            # Check for no two-hex rule: player cannot place the first piece on the second turn.
            # if self.turn_count == 1 and (piece == 'bee' and self.pieces[self.current_player]['bee'] == 1):
            #     print(f"Cannot place a piece on a hex adjacent to another piece. This violates the no-two-hex rule.")
            #     return
            
            # Ensure the Queen Bee must be placed by turn 4 but can be placed before.
            if status.turn_count >= 3 and status.pieces[status.current_player]["bee"] == 1 and piece!= 'bee':
                print("Queen Bee must be placed by the end of your fourth turn!")
                piece="bee"
            


            if board and not any((nq, nr) in board.grid for nq, nr in MoveFilter.get_adjacent_hexes(q, r)):
                print(f"Cannot place piece at ({q}, {r}): must be adjacent to an existing piece.")
                return

            # Ensure the placement doesn't connect with the opponent's pieces on turn 1
            if status.turn_count > 1: 
                q,r=target_position
                for neighbour in MoveFilter.get_adjacent_hexes(q, r):
                    nq,nr=neighbour                   
                    if board.hasPieceAt(nq,nr):  # Check if the neighboring position has a piece
            # Check if the piece is not owned by the current player
                        if neighbour not in current_player.positions:  # Check if the neighbor is not owned by the current player
                            print(f"Cannot place piece next to an opponent's piece after the first turn.")
                            return
                 # Enforces rule after both players' first moves
               


            board[(q, r)] = (piece)
            current_player.add_position(target_position)
            current_player.update_remaining_pieces(piece)
            print(f"{current_player.capitalize()} placed {piece} at {target_position}.")
            status.nextTurn()

    
    
            
        

