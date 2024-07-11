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
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        #update board

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece



        #pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)


        #king castling (the king is already moved in the #update board by the time it hits this)
        #this will move the rook
        if isinstance(piece, King):
            if self.castling(initial,final):
                diff = final.col - initial.col
                #checking if left or right rook and setting to correct piece
                rook = piece.left_rook if (diff<0) else piece.right_rook
                self.move(rook, rook.moves[-1])


        piece.moved = True

        piece.clear_moves()

        self.last_move = move


    def castling(self,initial,final):
        #this is not executing the castling, but it's checking if the move the player is trying to execute is a castling move
        #if the king is moving two squares, then it's a castling move
        return abs(initial.col - final.col)==2

    def valid_move(self, piece, move):
                return move in piece.moves
    
    def check_promotion(self,piece, final):
        if final.row == 7 or final.row == 0:
            self.squares[final.row][final.col].piece = Queen(piece.color)

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
                        initial = Square(row,col)
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
                        initial = Square(row,col)
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
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        #create squares for new move
                        initial = Square(row,col)
                        final = Square(move_row,move_col)

                        #create new move
                        new_move = Move(initial, final)

                        #append new valid move
                        piece.add_move(new_move)
                        
                        
        def straightline_moves(incrs):
            #  for bishop, rook, and queen moves in a straight line
            #  the increments between their moves differ
            # incrs refers to how their their (row, col) values can be incremented differently to change their position
            for dir in incrs:
                possible_row = row + dir[0]
                possible_col = col + dir[1]

                while(Square.in_range(possible_row, possible_col)):
                    if self.squares[possible_row][possible_col].isempty_or_rival(piece.color):
                        #create squares for new move
                        initial = Square(row,col)
                        final = Square(possible_row,possible_col)

                        #create new move
                        new_move = Move(initial, final)

                        #append new valid move
                        piece.add_move(new_move)

                        if self.squares[possible_row][possible_col].has_rival_piece(piece.color):
                            break
                    else:
                        break

                    possible_row += dir[0]
                    possible_col += dir[1]

        



        def king_moves():
            adjs = [
                (row+1, col+1), (row-1, col+1), (row+1, col-1), (row-1,col-1), 
                (row, col+1), (row, col-1), (row+1, col), (row-1, col)
            ]
            #normal moves
            for move in adjs:
                move_row, move_col = move
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        #create squares for new move
                        initial = Square(row,col)
                        final = Square(move_row,move_col)

                        #create new move
                        new_move = Move(initial, final)

                        #append new valid move
                        piece.add_move(new_move)

            
            if not piece.moved:
                #queenside castling
                left_rook=self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            #castling not possible
                            if self.squares[row][c].has_piece():
                                break 

                            if c==3:
                                piece.left_rook = left_rook

                                #rook move
                                initial = Square(row,0)
                                final = Square(row,3)
                                move = Move(initial,final)
                                left_rook.add_move(move)

                                #king move
                                initial = Square(row,col)
                                final = Square(row,2)
                                move = Move(initial,final)
                                piece.add_move(move)

            #kingside castling
            if not piece.moved:
                #queenside castling
                right_rook=self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5,7):
                            #castling not possible
                            if self.squares[row][c].has_piece():
                                break 

                            if c==6:
                                piece.right_rook = right_rook

                                #rook move
                                initial = Square(row,7)
                                final = Square(row,5)
                                move = Move(initial,final)
                                right_rook.add_move(move)

                                #king move
                                initial = Square(row,col)
                                final = Square(row,6)
                                move = Move(initial,final)
                                piece.add_move(move)


        if isinstance(piece, Pawn): pawn_moves()

        elif isinstance(piece,Knight):knight_moves()
            
        elif isinstance(piece,Bishop): straightline_moves([
            (-1, 1), (-1, -1), (1, -1), (1,1)
        ])
        elif isinstance(piece,Rook): straightline_moves([
            (1,0), (-1,0), (0,1), (0,-1)
        ])
            
        elif isinstance(piece,Queen): straightline_moves([
            (-1, 1), (-1, -1), (1, -1), (1,1),
            (1,0), (-1,0), (0,1), (0, -1)
        ])
            
        elif isinstance(piece,King): king_moves()

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


    

        
