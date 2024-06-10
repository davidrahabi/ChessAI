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

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_rival(self, color):
        return self.isempty() or self.has_rival_piece(color)

    @staticmethod #can be called without an object of this class
    def in_range(*args): #can recieve as many params
        for arg in args:
             if arg < 0 or arg > 7:
                return False
        
        return True