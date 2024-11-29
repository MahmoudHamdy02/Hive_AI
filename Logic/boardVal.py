class HiveBoard:
    def __init__(self):
        self.board = {}  # Maps (q, r) to (piece, player)
        self.current_player = "white"
        self.pieces = {"white": {"bee": 1, "ant": 3, "grasshopper": 3, "beetle": 2}, 
                       "black": {"bee": 1, "ant": 3, "grasshopper": 3, "beetle": 2}}
        self.turn_count = 0  # Track the number of turns for the Queen Bee placement rule

            # 0 ant 1 ant 2 ant 3 grass 4 bee
            
    def add_piece(self, piece, q, r):
        if (q, r) in self.board:
            print(f"({q}, {r}) is already occupied!")
            return

        if piece not in self.pieces[self.current_player] or self.pieces[self.current_player][piece] <= 0:
            print(f"No more {piece}s available for {self.current_player}.")
            return
        # Needed to be checked 
        # Check for no two-hex rule: player cannot place the first piece on the second turn.
        if self.turn_count == 1 and (piece == 'bee' and self.pieces[self.current_player]['bee'] == 1):
            print(f"Cannot place a piece on a hex adjacent to another piece. This violates the no-two-hex rule.")
            return
        
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
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places a bee
    board.add_piece("bee", 0, -1)
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White places an ant
    board.add_piece("ant", 1, 0)
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places an ant
    board.add_piece("ant", -1, -1)
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White places another ant
    board.add_piece("ant", 2, 0)
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places another ant
    board.add_piece("ant", -2, -1)
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White moves the ant from (1, 0) to (1, 1)
    board.move_piece(1, 0, 1, 1)
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black moves the ant from (-1, -1) to (-1, -2)
    board.move_piece(-1, -1, -1, -2)
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White places a grasshopper
    board.add_piece("grasshopper", 2, 1)
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places a beetle
    board.add_piece("beetle", -3, -1)
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White moves the grasshopper from (2, 1) to (2, -1) (jumping over black pieces)
    board.move_piece(2, 1, 2, -1)
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black moves the beetle from (-3, -1) to (-3, 0)
    board.move_piece(-3, -1, -3, 0)
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White places a beetle
    board.add_piece("beetle", 3, 0)
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places a grasshopper
    board.add_piece("grasshopper", -2, 0)
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White moves the beetle from (3, 0) to (3, 1)
    board.move_piece(3, 0, 3, 1)
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black moves the grasshopper from (-2, 0) to (-2, 1) (jumping over white pieces)
    board.move_piece(-2, 0, -2, 1)
    
    # Player White's Moves
    print("\nWhite's Moves:")
    # White places the last piece, the Queen Bee
    board.add_piece("bee", 4, 0)
    
    # Player Black's Moves
    print("\nBlack's Moves:")
    # Black places the Queen Bee
    board.add_piece("bee", -4, 0)
    
    # Player White's next move: Moving pieces to surround Black's Queen Bee (creating victory condition)
    print("\nWhite's Move (To check victory condition):")
    board.move_piece(4, 0, 3, 0)  # Move piece next to the black Queen Bee
    board.move_piece(3, 0, 2, 0)  # Continue surrounding Black's Queen Bee
    
    # Check for victory condition
    victory_message = board.check_victory()
    print(victory_message)

# Run the test case
test_hive_game()



