from Game_Logic.Board.Board import Board

class MoveFilter:
    
    ADJACENT_HEXES = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    
    @staticmethod
    def get_adjacent_hexes(q, r):
        return [(q + dq, r + dr) for dq, dr in MoveFilter.ADJACENT_HEXES]
    
    @staticmethod
    def check_hive_continuity(board, move):
        if not board:
            return True

        visited = set()
        start = next(iter(board.grid.keys()))

        def dfs(node):
            visited.add(node)
            for neighbor in MoveFilter.get_adjacent_hexes(*node):
                if neighbor in board and neighbor not in visited:
                    dfs(neighbor)

        dfs(start)
        return len(visited) == len(board)

    @staticmethod
    def can_slide_out(q, r, board):
        """
        Check if a piece can slide out of its position. A piece can slide if it is not
        surrounded by two or more occupied hexes on opposite sides.
        """
        adjacent = MoveFilter.get_adjacent_hexes(q, r)
        occupied_neighbors = [(nq, nr) for nq, nr in adjacent if (nq, nr) in board]
        if len(occupied_neighbors) < 2:
            return True  # Not surrounded enough to block sliding

        for i in range(len(occupied_neighbors)):
            hex1 = occupied_neighbors[i]
            hex2 = occupied_neighbors[(i + 1) % len(occupied_neighbors)]
            if (hex1[0] - q, hex1[1] - r) != (-hex2[0] + q, -hex2[1] + r):
                return True  # Gaps exist between neighbors; sliding is possible

        return False

    @staticmethod
    def _can_add_piece(piece, q, r, board, pieces, current_player, turn_count):
        if (q, r) in board:
            return False

        if piece not in pieces[current_player] or pieces[current_player][piece] <= 0:
            return False

        if turn_count >= 3 and pieces[current_player]["bee"] == 1 and piece != 'bee':
            return False

        if board and not any((nq, nr) in board for nq, nr in MoveFilter.get_adjacent_hexes(q, r)):
            return False

        if turn_count > 1:
            if any(
                board.get((nq, nr), (None, None))[1] != current_player
                for nq, nr in MoveFilter.get_adjacent_hexes(q, r)
                if (nq, nr) in board
            ):
                return False

        return True

    @staticmethod
    def _can_move_piece(current_pos, q, r, board, current_player):
        if current_pos not in board or (q, r) in board:
            return False

        piece, player = board[current_pos]
        if player != current_player:
            return False

        if piece == "grasshopper":
            return MoveFilter._is_valid_grasshopper_move(current_pos, q, r, board)
        elif piece == "beetle":
            return True  # Beetle can move one hex and on top
        elif not MoveFilter.can_slide_out(*current_pos, board):
            return False

        board.pop(current_pos)
        hive_connected = MoveFilter.is_hive_connected(board)
        board[current_pos] = (piece, player)

        return hive_connected

    @staticmethod
    def get_valid_moves_for_piece(piece, current_pos, board, pieces, current_player, turn_count):
        q, r = current_pos

        if piece == "bee":
            possible_moves = MoveFilter.possible_moves_bee(q, r)
        elif piece == "grasshopper":
            possible_moves = MoveFilter.get_grasshopper_moves(q, r)
        elif piece == "ant":
            possible_moves = MoveFilter.get_ant_moves(q, r)
        elif piece == "beetle":
            possible_moves = MoveFilter.get_beetle_moves(q, r)
        else:
            print(f"Unknown piece type: {piece}")
            return []

        valid_moves = MoveFilter.validate_moves_list(current_pos, possible_moves, piece, board, pieces, current_player, turn_count)
        return valid_moves

    @staticmethod
    def validate_moves_list(current_pos, possible_moves, piece, board, pieces, current_player, turn_count):
        valid_moves = []
        for nq, nr in possible_moves:
            if current_pos is None:
                if MoveFilter._can_add_piece(piece, nq, nr, board, pieces, current_player, turn_count):
                    valid_moves.append((nq, nr))
            else:
                if MoveFilter._can_move_piece(current_pos, nq, nr, board, current_player):
                    valid_moves.append((nq, nr))
        return valid_moves

    @staticmethod
    def filter_moves(board, moves):
        """
        Filters moves based on multiple rules: hive continuity, sliding, and any other game rules.
        
        Args:
        - board (Board): The game board instance.
        - moves (list): List of potential moves [(q, r), ...].
        
        Returns:
        - list: List of valid moves that pass all checks.
        """
        valid_moves = []

        for move in moves:
            q, r = move
            
            # Check hive continuity
            if not MoveFilter.check_hive_continuity(board, move):
                continue

            # Check specific game rules (optional rule-checking example)
            if not MoveFilter.check_other_rules(board, move):
                continue

            # Check if a piece can slide out (based on the current hex status)
            if board.grid.get((q, r)) and not MoveFilter.can_slide_out(q, r, board):
                continue

            # If all checks pass, append the move to valid moves
            valid_moves.append(move)

        return valid_moves
