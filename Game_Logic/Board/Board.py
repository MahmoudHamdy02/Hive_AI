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

    def getNeighbors(self, position:tuple) -> list:
        """
        Returns a list of all neighboring pieces
        """

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        neighbors = []
        for dq, dr in directions:
            q, r = position[0] + dq, position[1] + dr
            if self.hasPieceAt(q, r):
                neighbors.append((q, r))
        return neighbors

    def commonspace(self,position1:tuple, position2:tuple)->list:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        free_places1=[]
        free_places2=[]
        for dq,dr in directions:
            q, r = position1[0] + dq, position1[1] + dr
            if not self.hasPieceAt(q, r):
                free_places1.append((q, r))
        for dq,dr in directions:
            q, r = position2[0] + dq, position2[1] + dr
            if not self.hasPieceAt(q, r):
                free_places2.append((q, r))
        common_positions = list(set(free_places1) & set(free_places2))
        if common_positions:
            return common_positions
        else:
            return None

    def getGrid(self):
        return self.grid
    
    def getPieceAt(self, q, r):
        return self.grid[(q,r)].getPieces()
    
