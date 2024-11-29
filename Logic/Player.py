from enum import Enum

# A enum representing the player's color
class Color(Enum):
    WHITE = 1
    BLACK = 2

class Player:
    def __init__(self, color):
        self.color = color