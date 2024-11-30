from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game_Logic.Board.Board import Board
    from Game_Logic.Player.Player import Player

class Piece:
    def __init__(self, owner, position=None):
        """
        Initializes a Generic Hive Piece

        """
        self.owner: Player = owner
        self.position: tuple = position

    def getMoves(self, board: Board) -> list:
        """
        Returns a list of all possible moves for the piece

        """
        raise NotImplementedError("getMoves() must be implemented by subclass")
    
    def getOwner(self) -> Player:
        """
        Returns the owner of the piece

        """
        return self.owner
    
    def move(self, q, r):
        """
        Moves the piece to the specified position

        """
        self.position = (q, r)