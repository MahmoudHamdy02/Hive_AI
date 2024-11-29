class Board:
    def __init__(self) -> None:
        self.grid = {} # (q, r): [Piece1, Piece2, ...]}

    def addPiece(self, piece, q, r) -> None:
        if (q,r) not in self.grid:
            self.grid[(q,r)] = []
        self.grid[(q,r)].append(piece)

    def movePiece(self, piece, q, r) -> None:
        self.grid[piece.position].remove(piece)
        self.addPiece(piece, q, r)
        piece.move(q, r)

    def hasPieceAt(self, q,r) -> bool:
        return ((q,r) in self.grid and len(self.grid[(q,r)]) > 0)
    
    def getPieceAt(self, q, r):
        return self.grid[(q,r)][-1]
    