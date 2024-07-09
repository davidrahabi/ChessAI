import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
"""
Game Class: shows board and pieces on screen, initializes board and mouse dragger objects
"""
class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    def show_bg(self,surface): #surface will be self.screen from main
        theme = self.config.theme


        #draw board
        for row in range(ROWS):
            for col in range(COLS):
                #color
                color = theme.bg.light if (row+col)%2==0 else theme.bg.dark
                #rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                #blit
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
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            #loop through all valid moves and blit them 
            for move in piece.moves:
                # color
                color = theme.moves.light if(move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                #rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                
                #blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self,surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial,final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark

                rect = (pos.col* SQSIZE, pos.row * SQSIZE , SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180) 

            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE , SQSIZE, SQSIZE)

            pygame.draw.rect(surface, color, rect, width=3)
            
    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]
        
                
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'


    def change_theme(self):
        self.config.change_theme()
        