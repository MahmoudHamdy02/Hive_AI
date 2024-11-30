from Game_Logic.Piece.Piece import Piece
from Game_Logic.Board.Cell import Cell

class Board:
    def __init__(self) -> None:
        self.grid = {} # (q, r): [Piece1, Piece2, ...]}

    def addPiece(self, piece: Piece, q: int, r: int) -> None:
        if (q,r) not in self.grid:
            self.grid[(q,r)] = Cell()
        self.grid[(q,r)].addPiece(piece)

    def movePiece(self, piece: Piece, q, r) -> None:
        self.grid[piece.position].removePiece(piece)
        self.addPiece(piece, q, r)
        
    def hasPieceAt(self, q,r) -> bool:
        return ((q,r) in self.grid and len(self.grid[(q,r)]) > 0)
    
    def get_neighbors(self, q: int, r: int) -> list:
        """
        Returns a list of all neighboring positions for a given hexagonal coordinate (q, r).

        """
        # Define the six possible neighbor offsets
        neighbor_offsets = [
            (1, 0), 
            (-1, 0), 
            (0, 1),  
            (0, -1),  
            (1, -1),  
            (-1, 1),  
        ]

        # Compute neighbors by applying each offset to the current position
        neighbors = [(q + dq, r + dr) for dq, dr in neighbor_offsets]

        return neighbors
