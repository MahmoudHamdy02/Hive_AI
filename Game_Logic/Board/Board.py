from Game_Logic.Piece.Piece import Piece
from Game_Logic.Board.Cell import Cell

class Board:
    def __init__(self) -> None:
        self.grid = {} # (q, r): [Piece1, Piece2, ...]}   
        self.noOfPieces = 0

    def addPiece(self, piece: Piece, q: int, r: int) -> None:
        if (q,r) not in self.grid:
            self.grid[(q,r)] = Cell()
        self.grid[(q,r)].addPiece(piece)
        piece.position = (q,r)

    def movePiece(self, piece: Piece, q, r) -> None:
        self.grid[piece.position].removePiece()
        self.addPiece(piece, q, r)
        
    def hasPieceAt(self, q,r) -> bool:
        return ((q,r) in self.grid.keys() and len(self.grid[(q,r)].getPiecesList()) > 0)

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
        return self.grid[(q,r)].getPiece()
    
    def setGrid(self, grid):
        self.grid = grid

    def getNoOfPiecesAt(self, q, r):
        return self.grid[(q,r)].noOfPieces()
    
    def removePieceTemp(self, q, r):
        self.grid[(q,r)].removePiece()
        self.noOfPieces -= 1

    def addPieceTemp(self, piece, q, r):
        self.grid[(q,r)].addPiece(piece)
        self.noOfPieces += 1