from const import *
from square import  Square
from piece import *
from move import Move
"""
Board class: creates board full of square objects, then adds the pieces to the board
"""

class Board:

    def __init__(self):
        self.squares = []
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    
    def calc_moves(self, piece, row, col):
        """
        calculates all valid moves for a piece from its position
        """
        
        def pawn_moves():
            possible_moves = []
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for move_row in range(start, end, piece.dir):
                #if the pawn hasnt moved, this loop will run twice  (because it can move forward to two different squares), 
                # if the pawn has moved, it will just run once
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        initial = Square(move_row,col)
                        final = Square(move_row, col)

                        #create new move
                        new_move = Move(initial, final)

                        #append new valid move
                        piece.add_move(new_move)
                    else: break #if the first square is blocked
                    
                else: break #break if out of range
                    
            #diagonal moves
            move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]

            for possible_col in possible_move_cols:
                if Square.in_range(move_row, possible_col):
                    if self.squares[move_row][possible_col].has_rival_piece(piece.color):
                        initial = Square(move_row,possible_col)
                        final = Square(move_row, possible_col)

                        #create new move
                        new_move = Move(initial, final)

                        #append new valid move
                        piece.add_move(new_move)

            
            


        def knight_moves():
            possible_moves = [
                (row-2, col-1), (row-2, col +1), (row+2, col-1), (row+2, col+1),
                (row-1, col+2), (row+1, col+2), (row+1, col-2), (row-1, col-2)
            ]

            for move in possible_moves:
                move_row, move_col = move
                if Square.in_range(move_row, move_col):
                    if (self.squares[move_row][move_col].isempty_or_rival(piece.color)):
                        #create squares for new move
                        initial = Square(row,col)
                        final = Square(move_row,move_col)

                        #create new move
                        new_move = Move(initial, final)

                        #append new valid move
                        piece.add_move(new_move)
                        
                        
                


        if isinstance(piece, Pawn): pawn_moves()

        elif isinstance(piece,Knight):knight_moves()
            
        elif isinstance(piece,Bishop):
            pass
        elif isinstance(piece,Rook):
            pass
        elif isinstance(piece,Queen):
            pass
        elif isinstance(piece,King):
            pass

    def _create(self): #an underscore before a method shows that they are private methods
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)] #each column will have a list of 8 zeros representing squares

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] =  Square(row,col) #created board full of square objects
                                                          #the square objects are replacing the 8 zeros above
                                        


    def _add_pieces(self,color):
        row_pawn, row_other = (6,7) if color == 'white' else (1,0)
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


    

        
