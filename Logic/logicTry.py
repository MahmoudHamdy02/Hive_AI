class HiveBoard:
    def __init__(self):
        self.board = {}  # Maps (q, r) to (piece, player)
        self.current_player = "white"
        self.pieces = {"white": {"bee": 1, "ant": 3, "grasshopper": 3, "beetle": 2}, 
                       "black": {"bee": 1, "ant": 3, "grasshopper": 3, "beetle": 2}}
        self.turn_count = 0  # Track the number of turns for the Queen Bee placement rule

            # 0 ant 1 ant 2 ant 3 grass 4 bee
            
    def possible_moves_bee(self, q, r):
        """
        Bee moves one space in any direction.
        """
        return [(nq, nr) for nq, nr in self.get_adjacent_hexes(q, r) if (nq, nr) not in self.board]                 
            
    def add_piece(self, piece, q, r):
        if (q, r) in self.board:
            print(f"({q}, {r}) is already occupied!")
            return

        if piece not in self.pieces[self.current_player] or self.pieces[self.current_player][piece] <= 0:
            print(f"No more {piece}s available for {self.current_player}.")
            return
        # Needed to be checked 
        # Check for no two-hex rule: player cannot place the first piece on the second turn.
        # if self.turn_count == 1 and (piece == 'bee' and self.pieces[self.current_player]['bee'] == 1):
        #     print(f"Cannot place a piece on a hex adjacent to another piece. This violates the no-two-hex rule.")
        #     return
        
        # Ensure the Queen Bee must be placed by turn 4 but can be placed before.
        if self.turn_count >= 3 and self.pieces[self.current_player]["bee"] == 1 and piece!= 'bee':
            print("Queen Bee must be placed by the end of your fourth turn!")
            return


        if self.board and not any((nq, nr) in self.board for nq, nr in self.get_adjacent_hexes(q, r)):
            print(f"Cannot place piece at ({q}, {r}): must be adjacent to an existing piece.")
            return

        # Ensure the placement doesn't connect with the opponent's pieces on turn 1
        if self.turn_count > 1:  # Enforces rule after both players' first moves
            if any(
                self.board.get((nq, nr), (None, None))[1] != self.current_player
                for nq, nr in self.get_adjacent_hexes(q, r)
                if (nq, nr) in self.board
            ):
                print(f"Cannot place piece next to an opponent's piece after the first turn.")
                return


        self.board[(q, r)] = (piece, self.current_player)
        self.pieces[self.current_player][piece] -= 1
        print(f"{self.current_player.capitalize()} placed {piece} at ({q}, {r}).")
        self.turn_count += 1
        self.current_player = "black" if self.current_player == "white" else "white"
        self.end_turn()

    def move_piece(self, q1, r1, q2, r2):
        if (q1, r1) not in self.board:
            print(f"No piece at ({q1}, {r1}) to move.")
            return

        piece, player = self.board[(q1, r1)]
        if player != self.current_player:
            print(f"It's not {player}'s turn.")
            return

        if (q2, r2) in self.board:
            print(f"Hex ({q2}, {r2}) is already occupied.")
            return

        if piece not in ["grasshopper", "beetle"] and not self.can_slide_out(q1, r1):
            print(f"{piece.capitalize()} at ({q1}, {r1}) cannot slide out.")
            return

        # Temporarily remove the piece to ensure the hive stays connected
        self.board.pop((q1, r1))
        if not self.is_hive_connected():
            self.board[(q1, r1)] = (piece, player)
            print(f"Cannot move {piece} from ({q1}, {r1}) to ({q2}, {r2}): hive would be disconnected.")
            return

        self.board[(q2, r2)] = (piece, player)
        print(f"{self.current_player.capitalize()} moved {piece} from ({q1}, {r1}) to ({q2}, {r2}).")
        self.current_player = "black" if self.current_player == "white" else "white"
        self.end_turn()

    def end_turn(self):
        if not self.has_valid_moves_or_placements():
            self.current_player = "black" if self.current_player == "white" else "white"    
            print(f"{self.current_player.capitalize()} cannot move or place a piece. Turn passes.")
        else:
            print(f"Now it's {self.current_player.capitalize()}'s turn.")

    def has_valid_moves_or_placements(self):
        # Check for valid placements
        for piece, count in self.pieces[self.current_player].items():
            if count > 0:
                for q, r in self.board.keys():
                    if any((nq, nr) not in self.board for nq, nr in self.get_adjacent_hexes(q, r)):
                        return True

        # Check for valid moves
        for (q, r), (piece, player) in self.board.items():
            if player == self.current_player and self.can_slide_out(q, r):
                for nq, nr in self.get_adjacent_hexes(q, r):
                    if (nq, nr) not in self.board:
                        return True

        return False

    def can_slide_out(self, q, r):
        """
        Check if a piece can slide out of its position. A piece can slide if it is not 
        surrounded by two or more occupied hexes on opposite sides.
        """
        adjacent = self.get_adjacent_hexes(q, r)
        occupied_neighbors = [(nq, nr) for nq, nr in adjacent if (nq, nr) in self.board]
        if len(occupied_neighbors) < 2:
            return True  # Not surrounded enough to block sliding

        for i in range(len(occupied_neighbors)):
            hex1 = occupied_neighbors[i]
            hex2 = occupied_neighbors[(i + 1) % len(occupied_neighbors)]
            if (hex1[0] - q, hex1[1] - r) != (-hex2[0] + q, -hex2[1] + r):
                return True  # Gaps exist between neighbors; sliding is possible

        return False

    def _can_add_piece(self, piece, q, r):
        if (q, r) in self.board:
            return False

        if piece not in self.pieces[self.current_player] or self.pieces[self.current_player][piece] <= 0:
            return False

        # Ensure Queen Bee is placed by the end of the fourth turn
        if self.turn_count >= 3 and self.pieces[self.current_player]["bee"] == 1 and piece != 'bee':
            return False

        if self.board and not any((nq, nr) in self.board for nq, nr in self.get_adjacent_hexes(q, r)):
            return False

        if self.turn_count > 1:
            if any(
                self.board.get((nq, nr), (None, None))[1] != self.current_player
                for nq, nr in self.get_adjacent_hexes(q, r)
                if (nq, nr) in self.board
            ):
                return False

        return True

    def _can_move_piece(self, current_pos, q, r):
        if current_pos not in self.board or (q, r) in self.board:
            return False

        piece, player = self.board[current_pos]
        if player != self.current_player:
            return False

        # Movement rules for Grasshopper, Beetle, etc.
        if piece == "grasshopper":
            return self._is_valid_grasshopper_move(current_pos, q, r)
        elif piece == "beetle":
            return True  # Beetle can move one hex and on top
        elif not self.can_slide_out(*current_pos):
            return False

        # Temporarily remove the piece to check hive connectivity
        self.board.pop(current_pos)
        hive_connected = self.is_hive_connected()
        self.board[current_pos] = (piece, player)  # Restore

        return hive_connected


    def get_valid_moves_for_piece(self, piece, current_pos):
        """
        Get valid moves for a specific piece on the board.

        Args:
        - piece (str): The type of the piece (e.g., 'bee', 'ant', 'grasshopper', 'beetle').
        - current_pos (tuple): The current position of the piece as (q, r).

        Returns:
        - list: A list of valid move coordinates [(q, r), ...].
        """
        q, r = current_pos

        # Determine possible moves based on the piece type
        if piece == "bee":
            possible_moves = self.possible_moves_bee(q, r)
        elif piece == "grasshopper":
            possible_moves = self.get_grasshopper_moves(q, r)
        elif piece == "ant":
            possible_moves = self.get_ant_moves(q, r)
        elif piece == "beetle":
            possible_moves = self.get_beetle_moves(q, r)
        else:
            print(f"Unknown piece type: {piece}")
            return []

        print(f"Possible moves for {piece} at {current_pos}: {possible_moves}")
        # Validate possible moves
        valid_moves = self.validate_moves_list(current_pos, possible_moves)
        
        return valid_moves

    # Last 
    def validate_moves_list(self, current_pos, possible_moves, piece=None):
        """
        Validate possible moves using the existing add_piece and move_piece logic.
        
        Args:
        - current_pos: Tuple (q, r) of the current position of the piece (None for add_piece scenario).
        - possible_moves: List of tuples [(q, r), ...] representing potential moves.
        - piece: Piece to be added or moved (only for add_piece scenarios).

        Returns:
        - List of valid moves [(q, r), ...].
        """
        valid_moves = []

        for nq, nr in possible_moves:
            if current_pos is None:  # Adding a piece
                if self._can_add_piece(piece, nq, nr):
                    valid_moves.append((nq, nr))
            else:  # Moving a piece
                if self._can_move_piece(current_pos, nq, nr):
                    valid_moves.append((nq, nr))

        return valid_moves
    
    ADJACENT_HEXES = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]

    def get_adjacent_hexes(self, q, r):
        return [(q + dq, r + dr) for dq, dr in self.ADJACENT_HEXES]

    def is_hive_connected(self):
        if not self.board:
            return True

        visited = set()
        start = next(iter(self.board.keys()))  # Start from any piece in the hive

        def dfs(node):
            visited.add(node)
            for neighbor in self.get_adjacent_hexes(*node):
                if neighbor in self.board and neighbor not in visited:
                    dfs(neighbor)

        dfs(start)
        return len(visited) == len(self.board)

    def check_victory(self):
        """Check if the opponent's Queen Bee is surrounded and thus the game is over."""
        for (q, r), (piece, player) in self.board.items():
            if piece == "bee" and player != self.current_player:
                # Check if the opponent's Queen Bee is surrounded
                adjacent = self.get_adjacent_hexes(q, r)
                occupied_neighbors = [(nq, nr) for nq, nr in adjacent if (nq, nr) in self.board]
                if len(occupied_neighbors) == 6:
                    return f"{self.current_player.capitalize()} wins by surrounding the opponent's Queen Bee!"
        return None
    


def test_hive_game():
    # Initialize the game board
    board = HiveBoard()
    
    # Player White's Moves
    print("White's Moves:")
    # White places a bee
    board.add_piece("bee", 0, 0)
    
    board.add_piece("ant", 1, 0)
  
    board.add_piece("ant", 0, -1)
    board.add_piece("bee", 2, -1)
    valid_moves_black = board.get_valid_moves_for_piece("bee", (2, -1));
    print(valid_moves_black)
    
  

    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places a bee
    board.add_piece("bee", 0, -1)
    print("Valid Moves for Bee at (0, -1):", board.get_valid_moves_for_piece("bee", (0, -1)))
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White places an ant
    board.add_piece("ant", 1, 0)
    print("Valid Moves for Ant at (1, 0):", board.get_valid_moves_for_piece("ant", (1, 0)))
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places an ant
    board.add_piece("ant", -1, -1)
    print("Valid Moves for Ant at (-1, -1):", board.get_valid_moves_for_piece("ant", (-1, -1)))
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White places another ant
    board.add_piece("ant", 2, 0)
    print("Valid Moves for Ant at (2, 0):", board.get_valid_moves_for_piece("ant", (2, 0)))
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places another ant
    board.add_piece("ant", -2, -1)
    print("Valid Moves for Ant at (-2, -1):", board.get_valid_moves_for_piece("ant", (-2, -1)))
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White moves the ant from (1, 0) to (1, 1)
    board.move_piece(1, 0, 1, 1)
    print("Valid Moves for Ant at (1, 1):", board.get_valid_moves_for_piece("ant", (1, 1)))
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black moves the ant from (-1, -1) to (-1, -2)
    board.move_piece(-1, -1, -1, -2)
    print("Valid Moves for Ant at (-1, -2):", board.get_valid_moves_for_piece("ant", (-1, -2)))
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White places a grasshopper
    board.add_piece("grasshopper", 2, 1)
    print("Valid Moves for Grasshopper at (2, 1):", board.get_valid_moves_for_piece("grasshopper", (2, 1)))
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places a beetle
    board.add_piece("beetle", -3, -1)
    print("Valid Moves for Beetle at (-3, -1):", board.get_valid_moves_for_piece("beetle", (-3, -1)))
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White moves the grasshopper from (2, 1) to (2, -1) (jumping over black pieces)
    board.move_piece(2, 1, 2, -1)
    print("Valid Moves for Grasshopper at (2, -1):", board.get_valid_moves_for_piece("grasshopper", (2, -1)))
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black moves the beetle from (-3, -1) to (-3, 0)
    board.move_piece(-3, -1, -3, 0)
    print("Valid Moves for Beetle at (-3, 0):", board.get_valid_moves_for_piece("beetle", (-3, 0)))

# Run the test
test_hive_game()




