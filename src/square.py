"""
Square class: for creating and holding info about each square's location and whether it contains a piece
"""
class Square:

    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col 
        self.piece = piece

    def has_piece(self):
        return self.piece != None #returns true if it has a piece and false otherwise