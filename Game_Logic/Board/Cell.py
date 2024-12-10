class Cell:
    def __init__(self, pieces=None):
        """
        Initializes a Cell object

        """
        self.pieces = pieces if pieces else []

    def addPiece(self, piece):
        """
        Adds a piece to the cell

        """
        self.pieces.append(piece)

    def removePiece(self):
        """
        Removes a piece from the cell

        """
        self.pieces.pop()

    def getPiece(self):
        """
        Returns the top piece in the cell

        """
        return self.pieces[-1]
    
    def getPiecesList(self):
        """
        Returns all the pieces in the cell

        """
        return self.pieces

    def __len__(self):
        return len(self.pieces)
        
    def clone(self):
        """
        Creates a deep copy of the cell
        """
        return Cell(self.pieces.copy())