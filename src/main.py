import pygame
import sys
from const import *
from game import Game

"""
Main Class: creates the screen and starts the game
            loops through events/moves and updates screen as game continues
"""
class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creates screen
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        game = self.game
        board = self.game.board
        screen = self.screen
        dragger = self.game.dragger
        while True:
            game.show_bg(screen)  #this loop will keep running and continually update the screen
            game.show_moves(screen)
            game.show_pieces(screen) #show pieces

            #extra update blit if a piece is being dragged to render it faster/smoother
            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get(): #looks through all possible game events (user actions)
                
                #if the user clicks
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    dragger.update_mouse(event.pos) #updates pos with position of the event click

                    clicked_row = dragger.mouseY // SQSIZE #moving along y axis affects what row you are on
                    clicked_col = dragger.mouseX // SQSIZE #moving along x axis affects what column you are on
                    
                    

                    #if clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece #saving ref to piece
                        board.calc_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(event.pos) #save initial position of piece
                        dragger.drag_piece(piece)

                        #show methods
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                    

                #if user moves mouse
                elif event.type == pygame.MOUSEMOTION: 
                    if dragger.dragging: #if the user has a piece currently clicked
                        dragger.update_mouse(event.pos)

                        #adding extra blit for background and pieces to create smoother animation when dragging
                        #show methods
                        game.show_bg(screen) 
                        game.show_moves(screen)
                        game.show_pieces(screen)

                        dragger.update_blit(screen) #blit depends on mouse position, so updated mouse first


                #if user unclicks mouse
                elif event.type == pygame.MOUSEBUTTONUP: 
                    dragger.undrag_piece(piece)

                #if event is a quit by the user, end game
                elif event.type ==pygame.QUIT: 
                    pygame.quit()
                    sys.exit()



            pygame.display.update() #updates screen

main = Main()

main.mainloop()