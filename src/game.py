import pygame
from const import *
from board import Board
from dragger import Dragger

"""
Game Class: shows board and pieces on screen, initializes board and mouse dragger objects
"""
class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    def show_bg(self,surface): #surface will be self.screen from main
        #draw board
        for row in range(ROWS):
            for col in range(COLS):
                if(row+col) % 2 == 0:
                    color = (234,235,200) #beige

                else:
                    color = (119,154,88) #dark green

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)


    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                #check if there is a piece on the square to display
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    #blit all pieces except a piece that is being dragged
                    if piece is not self.dragger.piece:
                        piece.set_texture(size = 80)
                        img = pygame.image.load(piece.texture) #load the pieces image
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE //2 #calculates center of the square the piece will be placed in

                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect) #blit displays the image using img and the destination rectangle



    #show moves of the piece that the user clicks on
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            #loop through all valid moves and blit them 
            for move in piece.moves:
                # color
                color = '#C86464' if(move.final.row + move.final.col) % 2 == 0 else '#C84646'
                #rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                
                #blit
                pygame.draw.rect(surface, color, rect)
                