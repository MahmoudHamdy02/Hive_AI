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

    def removePiece(self, piece):
        """
        Removes a piece from the cell

        """
        self.pieces.pop(piece)

    def getPieces(self):
        """
        Returns the pieces in the cell

        """
        return self.pieces[-1]

    def __len__(self):
        return len(self.pieces)
        