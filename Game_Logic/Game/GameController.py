from Game_Logic.Game.MoveFilter import MoveFilter
from Game_Logic.Game.GameStatus import GameStatus
from Game_Logic.Board.Board import Board
from Game_Logic.Player.Player import Player
from Game_Logic.Player.Color import Color

class GameController:
    def __init__(self):
        """
        Initializes the game controller with a game board.
        """
        self.board = Board()
        self.white_player = Player(Color.WHITE)
        self.black_player = Player(Color.BLACK)
        self.status = GameStatus(self.board, self.white_player, self.black_player)


    def get_valid_adds(self, piece_type: str):
        if self.status.turn_count == 0:
            return [(0, 0)]
        valid_adds = []
        valid = True
        if self.status.turn_count >= 6 and len(self.status.getCurrentPlayer().get_remaining_pieces()["bee"]) == 1 and piece_type!= 'bee':
            print("Queen Bee must be placed by the end of your fourth turn!")
            return None
        for position in self.board.getGrid().keys():
            if not self.board.hasPieceAt(position[0], position[1]):
                continue
            for empty_neighbour in MoveFilter.get_adjacent_hexes(position[0], position[1]):
                if not self.board.hasPieceAt(empty_neighbour[0], empty_neighbour[1]):
                    if self.status.turn_count > 1: 
                        q,r=empty_neighbour
                        valid = True
                        for piece_neighbour in self.board.getNeighbors((q, r)):
                            piece_neighbour = self.board.getPieceAt(piece_neighbour[0], piece_neighbour[1])
                            if piece_neighbour.getOwner() != self.status.getCurrentPlayer():
                                valid = False
                        if valid:
                            valid_adds.append(empty_neighbour)
                    else:
                        valid_adds.append(empty_neighbour)
        return list(set(valid_adds))

    def get_valid_moves(self, position):
        """
        Gets valid moves for a specific piece at a given position.
        Delegates move generation to the piece class and validation to MoveFilter.
        """
        # piece_classes = {
        #     'Grasshopper': Grasshopper,
        #     'Ant': Ant,
        #     'Bee': Bee,
        #     'Spider': Spider
        # }

        # if piece not in piece_classes:
        #     raise ValueError(f"Unknown piece type: {piece}")

        # Get the potential moves from the piece class
        if len(self.status.getCurrentPlayer().get_remaining_pieces()["bee"]) == 1:
            return []
        piece = self.board.getPieceAt(position[0], position[1])
        potential_moves =piece.getMoves(self.board)
        # print(potential_moves, piece)

        # Filter the moves using the MoveFilter class
        return MoveFilter.filter_moves(self.board, potential_moves, position)
    
    def move_piece(self, position, move):
        piece = self.board.getPieceAt(position[0], position[1])
        # print(position)
        # print(piece)
        # print(self.get_valid_moves(position))
        if move in self.get_valid_moves(position):
             self.board.movePiece(piece, move[0], move[1])
             self.status.nextTurn()
             print(f"{self.status.getCurrentPlayer().get_color} moved {piece} to {move}.")
        else:
             raise ValueError(f"Unknown piece type: {piece}")

    def add_piece(self, piece_type: str, target_position):
            q,r=target_position

            if len(self.status.getCurrentPlayer().get_remaining_pieces()[piece_type]) <= 0:
                print(f"No more {piece_type}s available for {self.status.current_player}.")
                return
            # Needed to be checked 
            # Check for no two-hex rule: player cannot place the first piece on the second turn.
            # if self.turn_count == 1 and (piece == 'bee' and self.pieces[self.current_player]['bee'] == 1):
            #     print(f"Cannot place a piece on a hex adjacent to another piece. This violates the no-two-hex rule.")
            #     return
            
            # Ensure the Queen Bee must be placed by turn 4 but can be placed before.
                # piece_type = "bee"

            # if self.board and not any((nq, nr) in self.board.grid.keys for nq, nr in MoveFilter.get_adjacent_hexes(q, r)):
            #     print(f"Cannot place piece at ({q}, {r}): must be adjacent to an existing piece.")
            #     return

            # Ensure the placement doesn't connect with the opponent's pieces on turn 1
        
                 # Enforces rule after both players' first moves
               
            if target_position not in self.get_valid_adds(piece_type):
                print(f"Cannot place piece at ({q}, {r})")
                return
            
            piece = self.status.getCurrentPlayer().get_remaining_pieces()[piece_type].pop()

            # board[(q, r)] = (piece)
            # current_player.add_position(target_position)
            # current_player.update_remaining_pieces(piece)
            self.board.addPiece(piece, q, r)
            self.board.noOfPieces += 1
            print(f"{self.status.getCurrentPlayer().get_color} placed {piece} at {target_position}.")
            self.status.nextTurn()

    def hasPlay(self) -> bool:
        for piece in self.status.getCurrentPlayer().get_remaining_pieces().values():
            if len(piece) > 0:
                return True
            
        for (q, r) in self.board.getGrid().keys():
            for piece in self.board.getPieceAt(q, r):
                if ((piece.getOwner() == self.status.getCurrentPlayer()) and self.get_valid_moves() > 0):
                    return True
        self.status.nextTurn()
        return False
    
    def get_current_player(self):
        if self.status.getCurrentPlayer() == self.white_player:
            return 1
        elif self.status.getCurrentPlayer() == self.black_player:
            return 2
    
    def get_winner(self):
        if self.status.check_victory():
            if self.status.getCurrentPlayer() == self.white_player:
                return 1
            elif self.status.getCurrentPlayer() == self.black_player:
                return 2
        return 0

    def get_board(self):
        return self.board
    

    def get_all_possible_moves(self,board):
        """
        Returns a list of all valid moves for all pieces of the current player on the board.
        """
        moves = []
        for (q, r) in board.getGrid().keys():
            if board.hasPieceAt(q, r):
                piece = board.getPieceAt(q, r)
                if piece and piece.getOwner() == self.status.getCurrentPlayer():
                    # Get all valid moves for this piece
                    piece_moves = self.get_valid_moves((q, r))
                    # Store these moves
                    for move in piece_moves:
                        moves.append(((q, r), move))
        return moves
    
    def get_all_possible_adds(self):
        adds = []
        for piece_type, remaining_pieces in self.status.getCurrentPlayer().get_remaining_pieces().items():
            if remaining_pieces:  # Check if there are any pieces left of this type
                valid_add_positions = self.get_valid_adds(piece_type)
                for position in valid_add_positions:
                    adds.append((piece_type, position))  # (piece_type, target_position)
        return adds
    
    def change_board(self, new_board):
        self.board = new_board

    
    def count_pieces_around_opposite_queen(self):
        count = 0
        for (q, r) in self.board.getGrid().keys():
            if self.board.hasPieceAt(q, r):
                piece = self.board.getPieceAt(q, r)
                if piece.getOwner() != self.status.getCurrentPlayer() and piece == 'bee':
                    count = len(self.board.getNeighbors((q,r)))
        return count

    def count_pieces_around_my_queen(self):
        count = 0
        for (q, r) in self.board.getGrid().keys():
            if self.board.hasPieceAt(q, r):
                piece = self.board.getPieceAt(q, r)
                if piece.getOwner() == self.status.getCurrentPlayer() and piece == 'bee':
                    count = len(self.board.getNeighbors((q,r)))
        return count