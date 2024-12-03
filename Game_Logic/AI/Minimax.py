import sys
import os

# Add the root directory of the project to the Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_dir)

from Game_Logic.Game.GameController import GameController
from Game_Logic.Board.Board import Board
from Game_Logic.Player.Player import Player
from Game_Logic.Player.Color import Color
from Game_Logic.Game.GameStatus import GameStatus
from Game_Logic.Piece.Ant import Ant
from Game_Logic.Piece.Bee import Bee
from Game_Logic.Piece.Spider import Spider
from Game_Logic.Piece.GrassHopper import Grasshopper
from Game_Logic.Piece.Beetle import Beetle

board = Board()
white_player = Player(Color.WHITE)
black_player = Player(Color.BLACK)
game = GameStatus(board, white_player, black_player)
controller = GameController()

# Create pieces for white player
white_ant = Ant(white_player)
white_bee = Bee(white_player)
white_spider = Spider(white_player)
white_beetle = Beetle(white_player)
white_grasshopper = Grasshopper(white_player)

# Create pieces for black player
black_ant = Ant(black_player)
black_bee = Bee(black_player)
black_spider = Spider(black_player)
black_beetle = Beetle(black_player)
black_grasshopper = Grasshopper(black_player)

# Add pieces to the board

controller.add_piece('ant', (0, 0))
# controller.add_piece( 'grasshopper', (1, 1))
controller.add_piece( 'bee', (0, 1))
# controller.add_piece(game, board, 'bee', (1, 1), black_player)
# controller.add_piece(game, board,'spider', (0, 2), white_player)
# controller.add_piece(game, board, 'ant', (1, 0), black_player)
# controller.add_piece(game, board, 'beetle', (0, 3), white_player)
# controller.add_piece(game, board, 'grasshopper', (0, 4), white_player)





# print(controller.get_valid_adds())
# ... (keep all the existing imports and initializations)

class Minimax:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def evaluate(self, game_state):
        # This is a simple evaluation function. You might want to make this more sophisticated.
        return len(game_state.board.getGrid())

    def minimax(self, game_state, depth, maximizing_player):
        if depth == 0 or game_state.check_victory():
            return self.evaluate(game_state)

        if maximizing_player:
            max_eval = float('-inf')
            for move in game_state.get_all_possible_moves():
                new_state = game_state.apply_move(move)
                eval = self.minimax(new_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in game_state.get_all_possible_moves():
                new_state = game_state.apply_move(move)
                eval = self.minimax(new_state, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_best_move(self, game_state):
        best_move = None
        best_eval = float('-inf')
        for move in game_state.get_all_possible_moves():
            new_state = game_state.apply_move(move)
            eval = self.minimax(new_state, self.max_depth - 1, False)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

# Example usage
minimax_ai = Minimax(max_depth=3)

# Simulate a few moves
controller.add_piece('ant', (0, 0))
controller.add_piece('bee', (0, 1))
controller.add_piece('spider', (1, -1))

# Get the current game state
current_state = game

# Use Minimax to get the best move
best_move = minimax_ai.get_best_move(current_state)

print(f"Best move according to Minimax: {best_move}")

# Apply the best move
if best_move:
    piece_type, from_pos, to_pos = best_move
    if from_pos is None:  # This is a new piece placement
        controller.add_piece(piece_type, to_pos)
    else:  # This is moving an existing piece
        controller.move_piece(from_pos, to_pos)

print("Board state after AI move:")
print(board.getGrid())