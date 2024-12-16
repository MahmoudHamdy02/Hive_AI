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
            # print("Queen Bee must be placed by the end of your fourth turn!")
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
        if not self.board.hasPieceAt(position[0], position[1]):
            print(f"No piece at {position}.")
            return False
        piece = self.board.getPieceAt(position[0], position[1])
            
        if move in self.get_valid_moves(position):
             self.board.movePiece(piece, move[0], move[1])
            #  print(f"{self.status.getCurrentPlayer().get_color()} moved {piece} to {move}.")
             self.status.nextTurn()
             return True
        else:
             print(f"Unknown piece type: {piece}")
             return False

    def add_piece(self, piece_type: str, target_position):
            q,r=target_position

            if len(self.status.getCurrentPlayer().get_remaining_pieces()[piece_type]) <= 0:
                print(f"No more {piece_type}s available for {self.status.current_player}.")
                return False
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
               
            # if target_position not in self.get_valid_adds(piece_type):
                # print(f"Cannot place piece at ({q}, {r})")
                # return False
            
            piece = self.status.getCurrentPlayer().get_remaining_pieces()[piece_type].pop()

            # board[(q, r)] = (piece)
            # current_player.add_position(target_position)
            # current_player.update_remaining_pieces(piece)
            self.board.addPiece(piece, q, r)
            self.board.noOfPieces += 1
            # print(f"{self.status.getCurrentPlayer().get_color()} placed {piece} at {target_position}.")
            self.status.nextTurn()
            return True

    def hasPlay(self) -> bool:
        for piece in self.status.getCurrentPlayer().get_remaining_pieces().values():
            if len(piece) > 0:
                return True
            
        for (q, r) in self.board.getGrid().keys():
            if not self.board.hasPieceAt(q, r):
                continue
            piece = self.board.getPieceAt(q, r)
            if ((piece.getOwner() == self.status.getCurrentPlayer()) and self.get_valid_moves() > 0):
                return True
        self.status.nextTurn()
        return False
    
    def get_current_player(self):
        if self.status.getCurrentPlayer() == self.white_player:
            return 1
        elif self.status.getCurrentPlayer() == self.black_player:
            return 2
    
    def get_loser(self) -> int:
        # if self.status.check_victory():
        #     if self.status.getCurrentPlayer() == self.white_player:
        #         return 1
        #     elif self.status.getCurrentPlayer() == self.black_player:
        #         return 2
        # return 0
        return self.status.check_defeat()

    def get_board(self):
        return self.board
    
    def get_status(self):
        return self.status

    def get_all_moves_and_adds(self) -> list:
        all_moves_and_adds = []
        
        # Get moves
        grid_keys = list(self.board.getGrid().keys())
        for current_position in grid_keys:
            if not self.board.hasPieceAt(current_position[0], current_position[1]):
                continue

            piece = self.board.getPieceAt(current_position[0], current_position[1])
            if not piece or piece.getOwner() != self.status.getCurrentPlayer():
                continue
                
            valid_moves = self.get_valid_moves(current_position)
            if valid_moves:
                for new_position in valid_moves:
                    all_moves_and_adds.append([
                        piece.__class__.__name__.lower(),
                        current_position,
                        new_position
                    ])
        
        # Get adds
        for piece_type, pieces in self.status.getCurrentPlayer().get_remaining_pieces().items():
            if len(pieces) == 0: 
                continue
                
            valid_adds = self.get_valid_adds(piece_type)
            if valid_adds:
                for new_position in valid_adds:
                    all_moves_and_adds.append([
                        piece_type,
                        None,
                        new_position
                    ])

        return all_moves_and_adds
    
    def restore_state(self, state):
        if state['player_color'] == Color.WHITE:
            self.status.setCurrentPlayer(self.white_player)
        else:
            self.status.setCurrentPlayer(self.black_player)

        self.status.setTurnNumber(state['turn'])
        self.board.setGrid(state['grid'])
        self.white_player.set_remaining_pieces(state['pieces']['white'])
        self.black_player.set_remaining_pieces(state['pieces']['black'])