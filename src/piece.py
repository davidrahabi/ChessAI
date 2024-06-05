import os
class Piece:

    def __init__(self, name, color, value, texture = None, texture_rect = None):
        self.name = name
        self.color = color

        value_sign =1 if color == 'white' else -1 #white pieces have positive values, black pieces have negative values
        self.value = value * value_sign
        self.moves = [] #valid moves
        self.moved = False 
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
    
    def set_texture(self, size = 80):
        #access image of the piece
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png'
        )

    def add_moves(self, move): #append move to moves attribute
        self.moves.append(move)

class Pawn(Piece): #pawn inherits piece class

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
                          #direction that the pawn travels is dependent on its color
                          #in pygame, the x axis increases going to the right, and the y axis 
                          #going downwards starting from the top row

        super().__init__('pawn', color, 1.0)     #call piece class init method

class Knight(Piece):
     def __init__(self, color):
        super().__init__("knight", color, 3.0)

class Bishop(Piece):
     def __init__(self, color):
        super().__init__("bishop", color, 3.001)

class Rook(Piece):
     def __init__(self, color):
        super().__init__("rook", color, 5.0)

class King(Piece):
     def __init__(self, color):
        super().__init__("king", color, 10000)

class Queen(Piece):
     def __init__(self, color):
        super().__init__("queen", color, 9.0)
