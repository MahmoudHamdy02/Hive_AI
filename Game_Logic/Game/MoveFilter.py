from Game_Logic.Board.Board import Board
from Game_Logic.Game.GameStatus import status

class MoveFilter:
    
    ADJACENT_HEXES = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    
    @staticmethod
    def get_adjacent_hexes(q, r):
        return [(q + dq, r + dr) for dq, dr in MoveFilter.ADJACENT_HEXES]
    
    @staticmethod
    def check_hive_continuity(board, target_position,current_position=None):
       
        if not board or not board.grid:
            return True  # If the board is empty, any move is valid.


        # Get the piece to be moved
        piece = board.grid[current_position]

        def is_hive_continuous():
            visited = set()
            start = next(iter(board.grid.keys()))  # Get the first hex in the grid

            def dfs(node):
                visited.add(node)
                for neighbor in MoveFilter.get_adjacent_hexes(*node):
                    if neighbor in board.grid and neighbor not in visited:
                        dfs(neighbor)

            dfs(start)
            return len(visited) == len(board.grid)

        # Temporarily apply the move
        board.grid.pop(current_position)  # Remove the piece from its current position
        board.grid[target_position] = piece  # Place the piece at the new position

        # Check continuity
        is_continuous = is_hive_continuous()

        

        return is_continuous



    
    @staticmethod
    def can_slide_out( current_q, current_r,board):
        """
        Checks if the Ant can slide out from its current position.
        The Ant can slide out if there are no pieces blocking its path in any of the adjacent hexes.
        """
        # Check if the Ant is surrounded by pieces, meaning it cannot move.
        number_of_empty_cells=0
        for dq, dr in MoveFilter.ADJACENT_HEXES:
            adjacent_q = current_q + dq
            adjacent_r = current_r + dr

            # If there's no piece in this adjacent hex, the Ant can slide out
            if not board.hasPieceAt(adjacent_q, adjacent_r):
                number_of_empty_cells=number_of_empty_cells+1
                

        # If the Ant is surrounded by pieces in all adjacent hexes, it cannot move.
        if number_of_empty_cells >= 2:
            return True
        else :
            return False
        

    @staticmethod
    def can_slide_in(target_q, target_r, board):
        """
        Checks if a piece can slide into the target position.
        A piece can slide into the position if it is surrounded by fewer than 5 neighbors.

        :param target_q: The q-coordinate of the target hex.
        :param target_r: The r-coordinate of the target hex.
        :param board: The current board state.
        :return: True if the piece can slide into the position, False otherwise.
        """
        # Count the number of occupied neighbors around the target position
        occupied_neighbors = 0

        for dq, dr in MoveFilter.ADJACENT_HEXES:
            adjacent_q = target_q + dq
            adjacent_r = target_r + dr

            # Check if there is a piece in this adjacent hex
            if board.hasPieceAt(adjacent_q, adjacent_r):
                occupied_neighbors += 1

            # If already surrounded by 5 or more neighbors, return False early
            if occupied_neighbors >= 5:
                return False

        # If fewer than 5 neighbors are occupied, the piece can slide in
        return True
    
    @staticmethod
    def is_it_sliding(current_position, move, board):
        """
        Determines if a move is a sliding move.
        
        A sliding move occurs when the piece moves to a neighboring hex that is empty, 
        and it is connected to the current position by sliding over an occupied neighboring piece.

        Args:
        - current_position (tuple): The current position of the piece (q, r).
        - move (tuple): The move to check (target position) (q, r).
        - board (Board): The game board instance, which contains the grid and pieces.

        Returns:
        - bool: True if the move is a sliding move, False otherwise.
        """

        
        # Get empty neighbors of the current position (x)
        x = []
        q, r = current_position
        for dq, dr in MoveFilter.ADJACENT_HEXES:
            adjacent_q, adjacent_r = q + dq, r + dr
            if not board.hasPieceAt(adjacent_q, adjacent_r):  # Check if the adjacent cell is empty
                x.append((adjacent_q, adjacent_r))
        
        # Get occupied neighbors of the current position
        occupied_neighbors = []
        for dq, dr in MoveFilter.ADJACENT_HEXES:
            adjacent_q, adjacent_r = q + dq, r + dr
            if board.hasPieceAt(adjacent_q, adjacent_r):  # Check if the adjacent cell is occupied
                occupied_neighbors.append((adjacent_q, adjacent_r))
        
        # Get the empty neighbors of each occupied neighbor (y)
        y = []
        for occupied_q, occupied_r in occupied_neighbors:
            for dq, dr in MoveFilter.ADJACENT_HEXES:
                adjacent_q, adjacent_r = occupied_q + dq, occupied_r + dr
                if not board.hasPieceAt(adjacent_q, adjacent_r):  # Check if it's empty
                    y.append((adjacent_q, adjacent_r))
        
        # Find the intersection of x and y
        intersection = set(x).intersection(y)
        
        # Check if the move is in the intersection of x and y
        if move in intersection:
            return True  # It's a sliding move
        else:
            return False  # It's not a sliding move


          

    @staticmethod
    def filter_moves(board, moves,current_position):
        """
        Filters moves based on multiple rules: hive continuity, sliding, and any other game rules.
        
        Args:
        - board (Board): The game board instance.
        - moves (list): List of potential moves [(q, r), ...].
        
        Returns:
        - list: List of valid moves that pass all checks.
        """
        valid_move_sequences = []
        
        cq,cr=current_position
        #each element is a list of paths 

         # [1,2,3] -> [[1],[2],[3]]
         #[[1,2,3],[1,2,3]] -> [[1,2,3],[1,2,3]]

         # If moves is a 1D list, convert it into a 2D list for easier processing
        if all(isinstance(move, tuple) for move in moves):
            moves = [[move] for move in moves]

               
        for move_sequence in moves:
            valid_sequence = True
            temporary_position=current_position
        
        # Check each inner move in the spider's move sequence
            for move in move_sequence:
                q,r = move
            
                # Check hive continuity
                if not MoveFilter.check_hive_continuity(board, move,temporary_position):
                    valid_sequence = False
                    temporary_position=move
                    break  # Stop checking further moves in this sequence
                
                temporary_position=move


                # Check if a piece can slide out (based on the current hex status)
                if board.hasPieceAt((q, r)):
                    valid_sequence = False
                    break

                if not MoveFilter.can_slide_out(cq, cr, board) or not MoveFilter.can_slide_in(q, r, board):
                    valid_sequence = False
                    break
                if not MoveFilter.is_it_sliding(current_position, move, board):
                    valid_sequence = False
                    break

            # If all checks pass, append the move to valid moves
            if valid_sequence:
                valid_move_sequences.append(move_sequence)
            # Restore the board
            piece = board.grid[temporary_position]
            board.grid.pop(temporary_position)  # Remove the piece from the new position
            board.grid[current_position] = piece  # Restore the piece to its original position    

        return valid_move_sequences



        def add_piece(status,board, piece, q, r):
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
                return


            if board and not any((nq, nr) in board.grid for nq, nr in MoveFilter.get_adjacent_hexes(q, r)):
                print(f"Cannot place piece at ({q}, {r}): must be adjacent to an existing piece.")
                return

            # Ensure the placement doesn't connect with the opponent's pieces on turn 1
            if status.turn_count > 1:  # Enforces rule after both players' first moves
                if any(
                    board.get((nq, nr), (None, None))[1] != status.current_player
                    for nq, nr in MoveFilter.get_adjacent_hexes(q, r)
                    if (nq, nr) in board
                ):
                    print(f"Cannot place piece next to an opponent's piece after the first turn.")
                    return


            board[(q, r)] = (piece, status.current_player)
            status.pieces[status.current_player][piece] -= 1
            print(f"{self.current_player.capitalize()} placed {piece} at ({q}, {r}).")
            status.turn_count += 1
            status.current_player = "black" if status.current_player == "white" else "white"
            