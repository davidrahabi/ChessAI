from const import *
from square import  Square
from piece import *
"""
Board class: creates board full of square objects, then adds the pieces to the board
"""

class Board:

    def __init__(self):
        self.squares = []
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def _create(self): #an underscore before a method shows that they are private methods
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)] #each column will have a list of 8 zeros representing squares

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] =  Square(row,col) #created board full of square objects
                                                          #the square objects are replacing the 8 zeros above
                                        


    def _add_pieces(self,color):
        row_pawn, row_other = {6,7 } if color == 'white' else {1,0} 
        # white pawns will be on row 6, other pieces withll be on row 7, black pieces on rows 1 and 0

        #adding pawns
        for col in range(COLS): 
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #knights

        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #bishops

        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #King
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        
        #queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        
