from Game_Logic.Game.MoveFilter import MoveFilter

class GameController:
    def _init_(self, board,status):
        """
        Initializes the game controller with a game board.
        """
        self.board = board
        self.status=status


    def get_valid_adds(self):
        if self.status.turn_count == 0:
            return [(0, 0)]
        valid_adds = []
        valid = True
        for position in self.board.getGrid().keys():
            for empty_neighbour in MoveFilter.get_adjacent_hexes(position[0], position[1]):
                if not self.board.hasPieceAt(empty_neighbour[0], empty_neighbour[1]):
                    if self.status.turn_count > 1: 
                        q,r=empty_neighbour
                        for piece_neighbour in self.board.getNeighbors((q, r)):
                            if piece_neighbour.getOwner() != self.status.getCurrentPlayer():
                                valid = False
                        if valid:
                            valid_adds.append(empty_neighbour)
        return valid_adds

    def get_valid_moves(self, piece):
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
        potential_moves =piece.getMoves(self.board)

        # Filter the moves using the MoveFilter class
        return MoveFilter.filter_moves(self.board, potential_moves, piece.getPosition())
    
    def move_piece(self, move ,piece):
        if move in self.get_valid_moves(piece):
             self.board.movePiece(piece, move[0], move[1])
             self.status.nextTurn()
        else:
             raise ValueError(f"Unknown piece type: {piece}")

    def add_piece(self, piece_type: str, target_position):
            q,r=target_position

            if len(self.status.getCurrentPlayer.get_remaining_pieces[piece_type]) <= 0:
                print(f"No more {piece_type}s available for {self.status.current_player}.")
                return
            # Needed to be checked 
            # Check for no two-hex rule: player cannot place the first piece on the second turn.
            # if self.turn_count == 1 and (piece == 'bee' and self.pieces[self.current_player]['bee'] == 1):
            #     print(f"Cannot place a piece on a hex adjacent to another piece. This violates the no-two-hex rule.")
            #     return
            
            # Ensure the Queen Bee must be placed by turn 4 but can be placed before.
            if self.status.turn_count >= 3 and len(self.status.getCurrentPlayer.get_remaining_pieces["bee"]) == 1 and piece!= 'bee':
                print("Queen Bee must be placed by the end of your fourth turn!")
                piece_type = "bee"

            # if self.board and not any((nq, nr) in self.board.grid.keys for nq, nr in MoveFilter.get_adjacent_hexes(q, r)):
            #     print(f"Cannot place piece at ({q}, {r}): must be adjacent to an existing piece.")
            #     return

            # Ensure the placement doesn't connect with the opponent's pieces on turn 1
        
                 # Enforces rule after both players' first moves
               
            if target_position not in self.get_valid_adds():
                print(f"Cannot place piece at ({q}, {r}): must be adjacent to an existing piece.")
                return
            
            piece = self.status.getCurrentPlayer().get_remaining_pieces[piece_type].pop()

            # board[(q, r)] = (piece)
            # current_player.add_position(target_position)
            # current_player.update_remaining_pieces(piece)
            self.board.addPiece(piece, q, r)
            print(f"{self.status.getCurrentPlayer().capitalize()} placed {piece} at {target_position}.")
            self.status.nextTurn()
