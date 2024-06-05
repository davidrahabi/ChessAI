import pygame
from const import *
from board import Board

class Game:

    def __init__(self):
        self.board = Board()

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
                    
                    
                    img = pygame.image.load(piece.texture) #load the pieces image
                    img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE //2 #calculates center of the square the piece will be placed in

                    piece.texture_rect = img.get_rect(center = img_center)
                    surface.blit(img, piece.texture_rect) #blit displays the image using img and the destination rectangle
