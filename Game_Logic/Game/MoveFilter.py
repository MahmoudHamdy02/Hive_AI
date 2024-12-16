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
        piece = board.getPieceAt(*current_position)
        # piece = board.grid[current_position]

        def is_hive_continuous():
            len_visted=[0]
            visited = set()
            iterator = iter(board.grid.keys())
            start = next(iterator)  # Get the first hex in the grid
            while not board.hasPieceAt(*start):
                start = next(iterator)

            def dfs(node):
                visited.add(node)
                for i in range(board.getNoOfPiecesAt(*node)):
                    len_visted[0]+=1
                for neighbor in MoveFilter.get_adjacent_hexes(*node):
                    if board.hasPieceAt(*neighbor) and neighbor not in visited:
                        dfs(neighbor)

            dfs(start)
            # print(len(visited), board.noOfPieces)
            # return len(visited) == board.noOfPieces
            # print(len_visted[0], board.noOfPieces)
            return len_visted[0] == board.noOfPieces
        
        #Check continuity if we temporarly removed the piece
        board.removePieceTemp(*current_position)
        removed_continuity = is_hive_continuous()
        board.addPieceTemp(piece, *current_position)

        # Temporarily apply the move
        board.movePiece(piece, *target_position)

        # board.grid.pop(current_position)  # Remove the piece from its current position
        # board.grid[target_position] = piece  # Place the piece at the new position


        # Check continuity
        is_continuous = is_hive_continuous()
        

        return is_continuous and removed_continuity



    
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
        

    # @staticmethod
    # def can_slide_in(target_q, target_r, board):
    #     """
    #     Checks if a piece can slide into the target position.
    #     A piece can slide into the position if it is surrounded by fewer than 5 neighbors.

    #     :param target_q: The q-coordinate of the target hex.
    #     :param target_r: The r-coordinate of the target hex.
    #     :param board: The current board state.
    #     :return: True if the piece can slide into the position, False otherwise.
    #     """
    #     # Count the number of occupied neighbors around the target position
    #     occupied_neighbors = 0

    #     for dq, dr in MoveFilter.ADJACENT_HEXES:
    #         adjacent_q = target_q + dq
    #         adjacent_r = target_r + dr

    #         # Check if there is a piece in this adjacent hex
    #         if board.hasPieceAt(adjacent_q, adjacent_r):
    #             occupied_neighbors += 1

    #         # If already surrounded by 5 or more neighbors, return False early
    #         if occupied_neighbors >= 5:
    #             return False

    #     # If fewer than 5 neighbors are occupied, the piece can slide in
    #     return True
    
    # @staticmethod
    # def can_slide_in(target_q, target_r, board):
    #     """
    #     Checks if a piece can slide into the target position.
    #     A piece can slide into the position if it is surrounded by fewer than 5 neighbors.
    #     """
    #     neighbors = MoveFilter.get_adjacent_hexes(target_q, target_r)
    #     occupied_neighbors = 0

    #     for i in range(len(neighbors)):
    #         left = neighbors[i]
    #         right = neighbors[(i + 2) % len(neighbors)]  # Wraps around to create pairs

            
    #         if board.hasPieceAt(*left) and board.hasPieceAt(*right):
    #             return False  

            
    #         if board.hasPieceAt(*left):
    #             occupied_neighbors += 1

            
    #         if occupied_neighbors >= 5:
    #             return False
    
        # return True  # Move is valid if it passes all checks
  
    
    @staticmethod
    def can_slide_in(current_q,current_r,target_q, target_r, board):
        """
        Checks if a piece can slide into the target position.
        A piece can slide into the position if:
        1. It has fewer than 5 occupied neighbors.
        2. The path into the hex is not obstructed.
        """
        neighbors = MoveFilter.get_adjacent_hexes(current_q, current_r)
        neighbors2 = MoveFilter.get_adjacent_hexes(target_q, target_r)
        
        # Count occupied neighbors
        occupied_neighbors = sum(1 for q, r in neighbors2 if board.hasPieceAt(q, r))
        if occupied_neighbors >= 6:
            return False
        if occupied_neighbors == 5 and not (current_q,current_r) in neighbors:
            return False

        # Check for unobstructed sliding path
        # for i, (neighbor_q, neighbor_r) in enumerate(neighbors):
        #     left = neighbors[i - 1] if i - 1 >= 0 else neighbors[-1]
        #     right = neighbors[(i + 1) % len(neighbors)]
            
        #     # If the target is free and adjacent to a sliding path
        #     if not board.hasPieceAt(neighbor_q, neighbor_r):
        #         if not board.hasPieceAt(left[0], left[1]) and not board.hasPieceAt(right[0], right[1]):
        #             return True
        path_direction_q=target_q-current_q
        path_direction_r=target_r-current_r
        hexes_length=len(MoveFilter.ADJACENT_HEXES)
        index=-1
        for i in range(hexes_length):
            if path_direction_q == MoveFilter.ADJACENT_HEXES[i][0] and path_direction_r == MoveFilter.ADJACENT_HEXES[i][1]:
             index=i
        left_piece=neighbors[(index-1+hexes_length)%hexes_length]
        right_piece=neighbors[(index+1+hexes_length)%hexes_length]
        if board.hasPieceAt(left_piece[0], left_piece[1]) and  board.hasPieceAt(right_piece[0], right_piece[1]):
            return False

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
        piece = board.getPieceAt(*current_position)  # Initialize piece here
        
        cq,cr=current_position
        # Check if it is trapped
        # around = MoveFilter.get_adjacent_hexes(cq, cr)
        # if len(board.getNeighbors(current_position)) > 1:
        #     for neighbor in board.getNeighbors(current_position):
        #         nq, nr = neighbor
        #         neighbor_direction_q=nq-cq
        #         neighbor_direction_r=nr-cr
        #         isolated = True
        #         index=-1
        #         for i in range(len(MoveFilter.ADJACENT_HEXES)):
        #             if neighbor_direction_q == MoveFilter.ADJACENT_HEXES[i][0] and neighbor_direction_r == MoveFilter.ADJACENT_HEXES[i][1]:
        #                 index=i
        #         left_of_neighbor=around[(index-1+len(around))%len(around)]
        #         right_of_neighbor=around[(index+1+len(around))%len(around)]
        #         if board.hasPieceAt(*left_of_neighbor) or board.hasPieceAt(*right_of_neighbor):
        #             isolated = False
        #         if isolated:
        #             print("piece trapped")
        #             return []
        #each element is a list of paths 

        

         # [1,2,3] -> [[1],[2],[3]]
         #[[1,2,3],[1,2,3]] -> [[1,2,3],[1,2,3]]

         # If moves is a 1D list, convert it into a 2D list for easier processing
        if all(isinstance(move, tuple) for move in moves):
            moves = [[move] for move in moves]

        print(len(moves))
        for move_sequence in moves:
            valid_sequence = True
            temporary_position=current_position
        
            # Check each inner move in the spider's move sequence
            for move in move_sequence:
                q,r = move
            

                # Check if a piece can slide out (based on the current hex status)
                # if board.hasPieceAt(q, r):
                #     valid_sequence = False
                #     break


                # if not MoveFilter.is_it_sliding(current_position, move, board):
                #     valid_sequence = False
                #     break

                # Check hive continuity
                if not MoveFilter.check_hive_continuity(board, move,temporary_position):
                    # print("hive continuity False")
                    valid_sequence = False
                    temporary_position=move
                    break  # Stop checking further moves in this sequence
                
                temporary_position=move

            # If all checks pass, append the move to valid moves
            if valid_sequence:
                valid_move_sequences.append(move_sequence[-1])
            # Restore the board
            piece = board.getPieceAt(*temporary_position)
            board.movePiece(piece, *current_position)
            
        valid_move_ins = []
        if piece.get_piece_type() == "Beetle":
            return valid_move_sequences
        for move in valid_move_sequences:
            slide_in = False
            has_move_neighbor = False
            # Get adjacent moves
            adjacent_moves = MoveFilter.get_adjacent_hexes(*move)
            for neighbor in adjacent_moves:
                if neighbor in valid_move_sequences:
                    has_move_neighbor = True
                    if MoveFilter.can_slide_in(*neighbor, *move, board):
                        slide_in = True
                        # valid_move_sequences.remove(move)
                        # break
            # if not slide_in and has_move_neighbor:
            #     valid_move_sequences.remove(move)
            if slide_in or not has_move_neighbor:
                # print(move ,"add")
                valid_move_ins.append(move)

        valid_move_sequences = valid_move_ins

            # piece = board.grid[temporary_position]
            # board.grid.pop(temporary_position)  # Remove the piece from the new position
            # board.grid[current_position] = piece  # Restore the piece to its original position    
        return valid_move_sequences



        